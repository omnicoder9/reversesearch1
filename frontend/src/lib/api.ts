export type SearchPayload = {
  username?: string;
  platform?: string;
  email?: string;
  phone?: string;
  full_name?: string;
  photo_url?: string;
  consent_confirmed: boolean;
};

export type SearchResult = {
  primary_identifier: string;
  accounts: Array<{ platform: string; url: string; confidence: number; rationale: string }>;
  mentions: Array<{ source: string; title: string; url: string; snippet: string; confidence: number }>;
  photo_matches: Array<{ source: string; url: string; confidence: number }>;
  graph_edges: Array<{ source: string; target: string; relation: string }>;
  risk_notes: string[];
};

const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function startSearch(payload: SearchPayload): Promise<string> {
  const res = await fetch(`${apiBase}/api/v1/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Search request failed (${res.status})`);
  const json = await res.json();
  return json.task_id as string;
}

export async function pollSearch(taskId: string): Promise<{ status: string; result?: SearchResult; error?: string }> {
  const res = await fetch(`${apiBase}/api/v1/search/${taskId}`);
  if (!res.ok) throw new Error(`Polling failed (${res.status})`);
  return res.json();
}
