import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, HTMLResponse
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

        return {
            "answer": answer,
            "citations": citations,
            "thread_id": thread_id,
            "run_id": result["run"].id,  # type: ignore[attr-defined]
            "assistant_id": assistant_id,
        }
    except (APIConnectionError, APIStatusError) as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    # Single-file UI for simplicity
    html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ERP Help Assistant</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{
      --bg: #0f172a;
      --panel: #111827;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #22d3ee;
      --accent2: #60a5fa;
      --danger: #f87171;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; padding: 0;
      background: radial-gradient(circle at 20% 20%, #0b1220, #0a0f1e 40%, #0b1220 75%),
                  linear-gradient(135deg, rgba(34,211,238,0.08), rgba(96,165,250,0.08));
      min-height: 100vh; color: var(--text); font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell;
    }}
    .wrap {{
      max-width: 980px; margin: 0 auto; padding: 24px;
    }}
    .card {{
      background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px; padding: 16px;
      backdrop-filter: blur(6px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
    }}
    .title {{
      display: flex; align-items: center; gap: 12px; margin-bottom: 12px;
    }}
    .title h1 {{ margin: 0; font-size: 20px; font-weight: 600; letter-spacing: 0.2px; }}
    .badge {{
      font-size: 12px; color: var(--muted); padding: 2px 8px; border: 1px solid rgba(255,255,255,0.1); border-radius: 999px;
      background: rgba(255,255,255,0.02);
    }}
    .row {{ display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
    .row input[type="text"] {{
      flex: 1; min-width: 280px; padding: 12px 14px; border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.12); background: rgba(17,24,39,0.6); color: var(--text);
      outline: none; box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    }}
    .btn {{
      padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.14);
      background: linear-gradient(180deg, rgba(34,211,238,0.15), rgba(96,165,250,0.15));
      color: var(--text); cursor: pointer; font-weight: 600; letter-spacing: 0.2px;
    }}
    .btn:hover {{ filter: brightness(1.1); }}
    .btn.alt {{
      background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    }}
    .log {{
      margin-top: 14px; padding: 12px; font-size: 13px; color: var(--muted);
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
      max-height: 160px; overflow: auto;
    }}
    .chat {{ margin-top: 16px; display: grid; gap: 12px; }}
    .bubble {{
      padding: 12px 14px; border-radius: 12px; line-height: 1.45; white-space: pre-wrap;
      border: 1px solid rgba(255,255,255,0.08);
    }}
    .user {{ background: rgba(34,211,238,0.08); }}
    .assistant {{ background: rgba(96,165,250,0.10); }}
    .meta {{ margin-top: 6px; font-size: 12px; color: var(--muted); }}
    .sources a {{
      color: var(--accent); text-decoration: none; border-bottom: 1px dashed rgba(34,211,238,0.4);
    }}
    .sources a:hover {{ color: var(--accent2); border-color: rgba(96,165,250,0.6); }}
    .error {{ color: var(--danger); }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="title">
        <h1>ERP Help Assistant</h1>
        <span class="badge" id="status">Not initialized</span>
      </div>
      <div class="row" style="margin-bottom: 10px;">
        <button class="btn" onclick="runSetup()">Setup</button>
        <button class="btn alt" onclick="resetThread()">New Session</button>
      </div>
      <div class="row">
        <input id="q" type="text" placeholder="Ask a question, e.g. How do I create a voucher and print a check?" onkeydown="if(event.key==='Enter'){ask()}" />
        <button class="btn" onclick="ask()">Ask</button>
      </div>
      <div id="log" class="log"></div>
      <div id="chat" class="chat"></div>
    </div>
  </div>

  <script>
    let threadId = null;
    let assistantId = null;

    function log(msg, isError=false) {{
      const el = document.getElementById('log');
      const div = document.createElement('div');
      div.textContent = msg;
      if (isError) div.classList.add('error');
      el.appendChild(div);
      el.scrollTop = el.scrollHeight;
    }}

    function setStatus(text) {{
      document.getElementById('status').textContent = text;
    }}

    async function runSetup(recreate=false) {{
      setStatus('Setting up...');
      try {{
        const res = await fetch('/setup', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ recreate }}),
        }});
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        assistantId = data.assistant_id;
        setStatus(`Ready with ${data.files_indexed} files`);
        log(`Assistant ready. Files indexed: ${data.files_indexed}`);
      }} catch (e) {{
        setStatus('Setup error');
        log('Setup failed: ' + e.message, true);
      }}
    }}

    function addBubble(text, who='assistant', citations=[]) {{
      const chat = document.getElementById('chat');
      const wrap = document.createElement('div');
      const bubble = document.createElement('div');
      bubble.className = 'bubble ' + who;
      bubble.textContent = text;
      wrap.appendChild(bubble);

      if (who === 'assistant' && citations && citations.length) {{
        const meta = document.createElement('div');
        meta.className = 'meta sources';
        const parts = ['Sources: '];
        for (let i = 0; i < citations.length; i++) {{
          const c = citations[i];
          const a = document.createElement('a');
          a.href = c.url;
          a.target = '_blank';
          a.rel = 'noopener';
          a.textContent = c.filename;
          meta.appendChild(document.createTextNode(i === 0 ? 'Sources: ' : ', '));
          meta.appendChild(a);
        }}
        wrap.appendChild(meta);
      }}

      chat.appendChild(wrap);
      chat.scrollTop = chat.scrollHeight;
    }}

    async function ask() {{
      const input = document.getElementById('q');
      const question = input.value.trim();
      if (!question) return;
      input.value = '';

      addBubble(question, 'user');

      try {{
        const res = await fetch('/ask', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            question,
            thread_id: threadId
          }}),
        }});
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        threadId = data.thread_id;
        assistantId = data.assistant_id;
        addBubble(data.answer || 'Not covered in our docs.', 'assistant', data.citations || []);
      }} catch (e) {{
        log('Ask failed: ' + e.message, true);
        addBubble('There was an error answering your question.', 'assistant');
      }}
    }}

    function resetThread() {{
      threadId = null;
      document.getElementById('chat').innerHTML = '';
      log('New session started.');
    }}

    // Auto-setup on first load
    runSetup(false);
  </script>
</body>
</html>
    """
    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)