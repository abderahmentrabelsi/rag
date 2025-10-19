import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI, APIConnectionError, APIStatusError

# Load environment variables
load_dotenv()

# Constants and paths
BASE_DIR = Path(__file__).resolve().parent.parent
HELP_DOCS_DIR = BASE_DIR / "help_docs"
STATE_DIR = Path(__file__).resolve().parent
STATE_FILE = STATE_DIR / "assistant_state.json"

# Ensure help docs exist
if not HELP_DOCS_DIR.exists():
    raise RuntimeError(f"Missing help docs directory: {HELP_DOCS_DIR}")

# Initialize OpenAI client (requires OPENAI_API_KEY in environment)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set. Create a .env file or export the variable in your shell.")
client = OpenAI()
# Approximate 2025 pricing for gpt-4o-mini (USD per token)
INPUT_PRICE_PER_TOKEN = 0.15 / 1_000_000  # $0.15 per 1M input tokens
OUTPUT_PRICE_PER_TOKEN = 0.60 / 1_000_000  # $0.60 per 1M output tokens

# FastAPI app
app = FastAPI(title="ERP Help Center Assistant", default_response_class=ORJSONResponse)

# CORS - adjust origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve raw docs for clickable citations
app.mount("/docs", StaticFiles(directory=str(HELP_DOCS_DIR), html=True), name="docs")


# ---------------------------
# Models
# ---------------------------

class SetupRequest(BaseModel):
    recreate: Optional[bool] = False


class SetupResponse(BaseModel):
    assistant_id: str
    vector_store_id: str
    files_indexed: int
    files: List[Dict[str, str]]


class AskRequest(BaseModel):
    question: str
    thread_id: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    citations: List[Dict[str, str]]
    thread_id: str
    run_id: str
    assistant_id: str
    meta: Dict[str, Any]


# ---------------------------
# State helpers
# ---------------------------

def _load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _list_markdown_files() -> List[Path]:
    files: List[Path] = []
    for p in sorted(HELP_DOCS_DIR.glob("*.md")):
        files.append(p)
    return files


# ---------------------------
# OpenAI Assistants setup
# ---------------------------

def _delete_previous_resources(state: Dict[str, Any]) -> None:
    # Best-effort clean-up; ignore errors
    try:
        if "assistant_id" in state:
            client.beta.assistants.delete(assistant_id=state["assistant_id"])
    except Exception:
        pass

    try:
        if "vector_store_id" in state:
            client.vector_stores.delete(vector_store_id=state["vector_store_id"])
    except Exception:
        pass


def _create_or_get_assistant_and_vector_store(recreate: bool = False) -> Dict[str, Any]:
    state = _load_state()

    if not recreate and "assistant_id" in state and "vector_store_id" in state:
        # Validate they still exist by attempting a lightweight retrieve
        try:
            client.beta.assistants.retrieve(assistant_id=state["assistant_id"])
            client.vector_stores.retrieve(vector_store_id=state["vector_store_id"])
            return state
        except Exception:
            # If retrieval fails, proceed to recreate them
            pass

    if recreate and state:
        _delete_previous_resources(state)
        state = {}

    # 1) Create a vector store
    vector_store = client.vector_stores.create(name="erp-help-docs")

    # 2) Upload and attach all Markdown files
    md_files = _list_markdown_files()
    file_streams = [open(str(p), "rb") for p in md_files]
    file_batch = None
    try:
        if file_streams:
            file_batch = client.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files=file_streams,
            )
    finally:
        # Ensure streams are closed
        for fs in file_streams:
            try:
                fs.close()
            except Exception:
                pass

    # 3) Create the Assistant with File Search tool attached
    instructions = (
        "You are an ERP help center assistant. Answer strictly from the provided help documentation. "
        "If the docs do not contain the answer, respond with: Not covered in our docs. "
        "Provide step-by-step guidance and list the exact menu paths users should click. "
        "Always include source citations indicating the document title and section. "
        "Do not invent steps or features. Keep answers concise, 1–2 short paragraphs unless a numbered list of steps is necessary."
    )

    assistant = client.beta.assistants.create(
        name="ERP Help Assistant",
        model="gpt-4o-mini",
        instructions=instructions,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        },
    )

    # Capture filenames for later citation lookup
    attached_files: List[Dict[str, str]] = []
    try:
        # Vector store files list may be large; we only need names we just uploaded
        if file_batch and hasattr(file_batch, "file_counts"):
            # Fallback to local list we uploaded
            for p in md_files:
                attached_files.append({"filename": p.name, "path": f"/docs/{p.name}"})
        else:
            for p in md_files:
                attached_files.append({"filename": p.name, "path": f"/docs/{p.name}"})
    except Exception:
        for p in md_files:
            attached_files.append({"filename": p.name, "path": f"/docs/{p.name}"})

    new_state = {
        "assistant_id": assistant.id,
        "vector_store_id": vector_store.id,
        "files": attached_files,
    }
    _save_state(new_state)
    return new_state


def _poll_run(thread_id: str, run_id: str, timeout_s: float = 120.0, interval_s: float = 0.7) -> Dict[str, Any]:
    start = time.time()
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        status = run.status  # type: ignore[attr-defined]
        if status in ("completed", "failed", "cancelled", "expired"):
            return {"status": status, "run": run}
        if status in ("requires_action",):
            # We are not using tools that require action; cancel such runs
            try:
                client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
            except Exception:
                pass
            return {"status": "cancelled", "run": run}
        if time.time() - start > timeout_s:
            try:
                client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
            except Exception:
                pass
            return {"status": "expired", "run": run}
        time.sleep(interval_s)


def _extract_answer_and_citations(thread_id: str) -> Dict[str, Any]:
    msgs = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=5)
    answer_text = ""
    file_ids: Set[str] = set()

    # Find the latest assistant message
    for m in msgs.data:
        if m.role == "assistant":
            # Message content may contain multiple items
            for item in m.content:
                if item.type == "text":
                    # Collect text
                    answer_text += item.text.value  # type: ignore[attr-defined]
                    # Collect citations
                    for ann in item.text.annotations:  # type: ignore[attr-defined]
                        try:
                            if ann.type == "file_citation":
                                file_ids.add(ann.file_citation.file_id)  # type: ignore[attr-defined]
                        except Exception:
                            continue
            break

    # Map file_ids to filenames
    citations: List[Dict[str, str]] = []
    for fid in file_ids:
        try:
            fi = client.files.retrieve(fid)
            fn = fi.filename or fid  # type: ignore[attr-defined]
        except Exception:
            fn = fid
        citations.append({
            "file_id": fid,
            "filename": fn,
            "url": f"/docs/{fn}",
        })

    return {"answer": answer_text.strip(), "citations": citations}


# ---------------------------
# Routes
# ---------------------------

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/setup", response_model=SetupResponse)
def setup(data: SetupRequest) -> Any:
    try:
        state = _create_or_get_assistant_and_vector_store(recreate=bool(data.recreate))
        files = state.get("files", [])
        return {
            "assistant_id": state["assistant_id"],
            "vector_store_id": state["vector_store_id"],
            "files_indexed": len(files),
            "files": files,
        }
    except (APIConnectionError, APIStatusError) as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=AskResponse)
def ask(data: AskRequest) -> Any:
    state = _load_state()
    if "assistant_id" not in state or "vector_store_id" not in state:
        raise HTTPException(status_code=400, detail="Setup not completed. Call /setup first.")

    assistant_id: str = state["assistant_id"]
    start_ts = time.perf_counter()

    # Validate vector store exists; if missing (404) recreate assistant + store
    try:
        client.vector_stores.retrieve(vector_store_id=state["vector_store_id"])
    except Exception:
        new_state = _create_or_get_assistant_and_vector_store(recreate=True)
        state = new_state
        assistant_id = state["assistant_id"]

    try:
        # Create or reuse a thread
        if data.thread_id:
            thread_id = data.thread_id
        else:
            thread = client.beta.threads.create()
            thread_id = thread.id  # type: ignore[attr-defined]

        # Add the user question
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=data.question,
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Poll until completion
        result = _poll_run(thread_id=thread_id, run_id=run.id)  # type: ignore[attr-defined]
        status = result["status"]
        if status != "completed":
            run_obj = result.get("run")
            err_msg = ""
            try:
                last_err = getattr(run_obj, "last_error", None)
                if last_err:
                    err_msg = f", error: {getattr(last_err, 'message', str(last_err))}"
            except Exception:
                pass
            raise HTTPException(status_code=502, detail=f"Run did not complete. Status: {status}{err_msg}")

        # Extract answer and citations
        parsed = _extract_answer_and_citations(thread_id=thread_id)
        answer = parsed["answer"]
        citations = parsed["citations"]

        # If assistant produced nothing, return controlled refusal
        if not answer:
            answer = "Not covered in our docs."

        # Metrics
        elapsed = time.perf_counter() - start_ts
        run_obj = result["run"]
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        try:
            usage = getattr(run_obj, "usage", None)
            if usage:
                # Support different SDK field names
                input_tokens = getattr(usage, "input_tokens", getattr(usage, "prompt_tokens", 0)) or 0
                output_tokens = getattr(usage, "output_tokens", getattr(usage, "completion_tokens", 0)) or 0
                total_tokens = getattr(usage, "total_tokens", (input_tokens + output_tokens)) or (input_tokens + output_tokens)
        except Exception:
            pass
        cost_usd = round(input_tokens * INPUT_PRICE_PER_TOKEN + output_tokens * OUTPUT_PRICE_PER_TOKEN, 6)
        meta = {
            "duration_seconds": round(elapsed, 4),
            "duration_ms": int(elapsed * 1000),
            "tokens": {"input": input_tokens, "output": output_tokens, "total": total_tokens},
            "cost_usd": cost_usd,
            "chunks": len(citations or []),
            "shots": 0,
            "model": "gpt-4o-mini",
        }
        return {
            "answer": answer,
            "citations": citations,
            "thread_id": thread_id,
            "run_id": run_obj.id,  # type: ignore[attr-defined]
            "assistant_id": assistant_id,
            "meta": meta,
        }
    except (APIConnectionError, APIStatusError) as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "React UI is served separately. Use the web client to interact with this API.",
        "docs_path": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)