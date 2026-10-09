import type { Example, Result } from "../types";
async function j<T>(r: Response): Promise<T> {
  if (!r.ok) { let d = `Request failed (${r.status})`; try { const b = await r.json(); d = typeof b.detail === "string" ? b.detail : "Invalid input. Check the form."; } catch {} throw new Error(d); }
  return r.json();
}
const net = (e: unknown): never => { throw e instanceof TypeError ? new Error("Cannot reach the backend. Is it running on port 8000?") : e; };
export const getExamples = () => fetch("/api/examples").then(r => j<Example[]>(r)).catch(net);
export const analyze = (b: { message: string; message_type: string; sender?: string; url?: string }) =>
  fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) }).then(r => j<Result>(r)).catch(net);
