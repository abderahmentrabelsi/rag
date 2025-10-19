import React from "react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "./components/ui/card";
import { Badge } from "./components/ui/badge";

type Citation = { filename: string; url: string };
type Meta = {
  duration_seconds: number;
  duration_ms: number;
  tokens: { input: number; output: number; total: number };
  cost_usd: number;
  chunks: number;
  shots: number;
  model: string;
  cached?: boolean;
};
type AskResponse = {
  answer: string;
  citations: Citation[];
  thread_id: string;
  run_id: string;
  assistant_id: string;
  meta?: Meta;
};

// Using Vite dev proxy from vite.config.ts, so relative paths are fine in dev
const API_BASE = "";

export default function App() {
  const [initialized, setInitialized] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [question, setQuestion] = React.useState("");
  const [messages, setMessages] = React.useState<
    { role: "user" | "assistant"; text: string; citations?: Citation[]; metaLine?: string; metaCached?: boolean }[]
  >([]);

  async function setup(recreate = false) {
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/setup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recreate }),
      });
      if (!res.ok) {
        const err = await res.text().catch(() => "");
        throw new Error(err || `Setup failed with ${res.status}`);
      }
      await res.json();
      setInitialized(true);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", text: `Setup error: ${e?.message || String(e)}` }]);
    } finally {
      setBusy(false);
    }
  }

  async function askStream() {
    const q = question.trim();
    if (!q) return;
    setQuestion("");
    // Add user message
    setMessages((m) => [...m, { role: "user", text: q }]);
    // Add empty assistant message to stream into
    setMessages((m) => [...m, { role: "assistant", text: "", citations: [], metaLine: undefined, metaCached: false }]);
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/ask/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      if (!res.ok || !res.body) {
        const err = await res.text().catch(() => "");
        throw new Error(err || `Stream failed with ${res.status}`);
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const frames = buffer.split("\n\n");
        buffer = frames.pop() || "";
        for (const raw of frames) {
          const lines = raw.split("\n");
          let event = "";
          let data = "";
          for (const line of lines) {
            if (line.startsWith("event:")) event = line.slice(6).trim();
            else if (line.startsWith("data:")) data += line.slice(5).trim();
          }
          if (!event) continue;
          if (event === "delta") {
            let payload: any;
            try { payload = JSON.parse(data); } catch { payload = { text: data }; }
            const chunk = payload?.text ?? "";
            if (chunk) {
              setMessages((m) => {
                const copy = [...m];
                const last = copy[copy.length - 1];
                if (last && last.role === "assistant") {
                  last.text = (last.text || "") + chunk;
                }
                return copy;
              });
            }
          } else if (event === "done") {
            let payload: any = {};
            try { payload = JSON.parse(data); } catch {}
            const citations: Citation[] = payload?.citations || [];
            const meta = payload?.meta;
            const metaLine = meta
              ? `Completed in ${meta.duration_seconds.toFixed(2)}s using ${meta.chunks} chunks and ${meta.shots} shots. Tokens in/out/total: ${meta.tokens.input}/${meta.tokens.output}/${meta.tokens.total}. Cost: $${meta.cost_usd.toFixed(6)}. Model: ${meta.model}.`
              : undefined;
            const isCached = !!meta?.cached;
            setMessages((m) => {
              const copy = [...m];
              const last = copy[copy.length - 1];
              if (last && last.role === "assistant") {
                last.citations = citations;
                last.metaLine = metaLine;
                last.metaCached = isCached;
              }
              return copy;
            });
          } else if (event === "error") {
            let payload: any = {};
            try { payload = JSON.parse(data); } catch {}
            setMessages((m) => [
              ...m,
              { role: "assistant", text: `Error: ${payload?.status || "Unknown error"}` },
            ]);
          }
        }
      }
    } catch (e: any) {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: `Error: ${e?.message || String(e)}` },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      <div className="mx-auto max-w-3xl p-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>ERP Help Assistant</CardTitle>
              <Badge className={initialized ? "border-green-500 text-green-700" : ""}>
                {initialized ? "Ready" : "Not initialized"}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex gap-2">
              <Button disabled={busy} onClick={() => setup(false)}>
                Setup
              </Button>
              <Button disabled={busy} variant="outline" onClick={() => setup(true)}>
                Reindex
              </Button>
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Ask a question, e.g., How do I enter a voucher?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => (e.key === "Enter" ? askStream() : undefined)}
              />
              <Button disabled={busy || !initialized} onClick={askStream}>Ask</Button>
            </div>

            <div className="space-y-4">
              {messages.map((m, i) => (
                <div key={i} className="rounded-md border p-3">
                  <div className="mb-1 text-xs text-muted-foreground">
                    {m.role === "user" ? "You" : "Assistant"}
                  </div>
                  <div className="whitespace-pre-wrap">{m.text}</div>

                  {/* Sources highlighted but NOT clickable */}
                  {m.citations && m.citations.length > 0 && (
                    <div className="mt-2 text-xs text-muted-foreground">
                      Sources:
                      <span className="ml-1">
                        {m.citations.map((c, idx) => (
                          <span
                            key={`${c.filename}-${idx}`}
                            className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-accent/40 text-muted-foreground mr-1"
                            title={c.filename}
                          >
                            {c.filename}
                          </span>
                        ))}
                      </span>
                    </div>
                  )}

                  {(m.metaLine || m.metaCached) && (
                    <div className="mt-1 text-xs text-muted-foreground flex items-center gap-2">
                      <span>{m.metaLine}</span>
                      {m.metaCached && (
                        <Badge className="border-amber-400 text-amber-700 bg-amber-100">Cached</Badge>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
          <CardFooter className="text-xs text-muted-foreground">
            Backend: proxied to http://localhost:8000
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}