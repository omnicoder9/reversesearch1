import { useEffect, useRef, useState } from "react";
import { ResultView } from "./components/ResultView";
import { SearchForm } from "./components/SearchForm";
import { pollSearch, startSearch, type SearchPayload, type SearchResult } from "./lib/api";

export function App() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>("idle");
  const [error, setError] = useState<string>("");
  const [result, setResult] = useState<SearchResult | null>(null);
  const taskIdRef = useRef<string>("");

  useEffect(() => {
    if (!taskIdRef.current) return;
    if (!(status === "PENDING" || status === "STARTED")) return;

    const timer = setInterval(async () => {
      try {
        const state = await pollSearch(taskIdRef.current);
        setStatus(state.status);
        if (state.status === "SUCCESS" && state.result) {
          setResult(state.result);
          setLoading(false);
          clearInterval(timer);
        }
        if (state.status === "FAILURE") {
          setError(state.error ?? "Search failed");
          setLoading(false);
          clearInterval(timer);
        }
      } catch (e) {
        setError((e as Error).message);
        setLoading(false);
        clearInterval(timer);
      }
    }, 1500);

    return () => clearInterval(timer);
  }, [status]);

  async function handleSubmit(payload: SearchPayload) {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const taskId = await startSearch(payload);
      taskIdRef.current = taskId;
      setStatus("PENDING");
    } catch (e) {
      setError((e as Error).message);
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <header>
        <h1>Reverse Search App</h1>
        <p>
          Aggregate public signals, estimate linkage confidence, and review risk notes before any action.
        </p>
      </header>
      <SearchForm onSubmit={handleSubmit} loading={loading} />
      <section className="status panel">
        <h2>Task Status</h2>
        <p className="muted">{status}</p>
        {error && <p className="error">{error}</p>}
      </section>
      {result && <ResultView result={result} />}
    </main>
  );
}
