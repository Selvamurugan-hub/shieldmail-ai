import { useEffect, useState } from "react";
import { Shield, ShieldAlert, ShieldCheck, ShieldQuestion, Moon, Sun, Trash2, Loader2 } from "lucide-react";
import { analyze, getExamples } from "./services/api";
import type { Example, HistoryItem, Result } from "./types";

const LVL = { Low: ["text-emerald-700 dark:text-emerald-300 border-emerald-500", ShieldCheck], Medium: ["text-amber-700 dark:text-amber-300 border-amber-500", ShieldQuestion],
  High: ["text-orange-700 dark:text-orange-300 border-orange-500", ShieldAlert], Critical: ["text-red-700 dark:text-red-300 border-red-500", ShieldAlert] } as const;
const KEY = "shieldmail-history";
const card = "rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5";

function ResultView({ r }: { r: Result }) {
  const [cls, Icon] = LVL[r.risk_level];
  return (
    <section className={card} aria-live="polite">
      <div className={`flex items-center gap-3 border-l-4 pl-3 ${cls}`}>
        <Icon aria-hidden /><div><p className="text-xl font-bold">{r.risk_level.toUpperCase()} RISK — {r.risk_score} / 100</p>
        <p className="text-sm">{r.verdict} · {r.evidence_strength}</p></div></div>
      <h3 className="mt-5 font-semibold">Evidence found</h3>
      {r.findings.length === 0 && <p className="text-sm text-slate-500">No indicators matched.</p>}
      <ul className="mt-2 space-y-3">{r.findings.map((f, i) => (
        <li key={i} className="text-sm"><b>{f.title}</b> <span className="text-slate-500">({f.severity}, +{f.points_contributed})</span>
          <p>{f.description}</p><code className="block mt-1 rounded bg-slate-100 dark:bg-slate-800 p-1 break-words">{f.evidence}</code></li>))}</ul>
      <h3 className="mt-5 font-semibold">Recommended actions</h3>
      <ol className="list-decimal ml-5 text-sm space-y-1">{r.recommendations.map((x, i) => <li key={i}>{x}</li>)}</ol>
      <h3 className="mt-5 font-semibold">Method and limitations</h3>
      <p className="text-sm">Analysis mode: {r.analysis_mode}. {r.model_status.detail}</p>
      <ul className="list-disc ml-5 text-sm text-slate-600 dark:text-slate-400">{r.limitations.map((x, i) => <li key={i}>{x}</li>)}</ul>
    </section>);
}

export default function App() {
  const [page, setPage] = useState("Dashboard");
  const [dark, setDark] = useState(true);
  const [examples, setExamples] = useState<Example[]>([]);
  const [msg, setMsg] = useState(""); const [sender, setSender] = useState(""); const [url, setUrl] = useState(""); const [type, setType] = useState("email");
  const [label, setLabel] = useState<string | null>(null);
  const [res, setRes] = useState<Result | null>(null); const [err, setErr] = useState(""); const [busy, setBusy] = useState(false);
  const [hist, setHist] = useState<HistoryItem[]>(() => { try { return JSON.parse(sessionStorage.getItem(KEY) || "[]"); } catch { return []; } });
  useEffect(() => { document.documentElement.classList.toggle("dark", dark); }, [dark]);
  useEffect(() => { getExamples().then(setExamples).catch(() => {}); }, []);
  useEffect(() => { try { sessionStorage.setItem(KEY, JSON.stringify(hist)); } catch {} }, [hist]);

  const load = (e: Example) => { setMsg(e.message); setSender(e.sender || ""); setType(e.message_type); setUrl(""); setLabel(e.label); setPage("Analyze Message"); };
  const run = async () => {
    setErr(""); if (!msg.trim()) { setErr("Please paste a message first."); return; }
    setBusy(true);
    try { const r = await analyze({ message: msg, message_type: type, sender: sender || undefined, url: url || undefined });
      setRes(r); setHist([{ id: r.analysis_id, at: new Date().toLocaleString(), type, result: r }, ...hist].slice(0, 50)); setPage("Analyze Message");
    } catch (e) { setErr((e as Error).message); } finally { setBusy(false); }
  };
  const clear = () => { setMsg(""); setSender(""); setUrl(""); setLabel(null); setRes(null); setErr(""); };
  const stats = { n: hist.length, high: hist.filter(h => h.result.risk_score >= 50).length, avg: hist.length ? Math.round(hist.reduce((a, h) => a + h.result.risk_score, 0) / hist.length) : 0 };

  const form = (
    <div className={card}>
      {label && <p className="mb-2 text-xs rounded bg-cyan-100 dark:bg-cyan-950 text-cyan-800 dark:text-cyan-200 px-2 py-1 inline-block">Synthetic example: {label}</p>}
      <label className="block text-sm font-medium" htmlFor="m">Message</label>
      <textarea id="m" value={msg} onChange={e => setMsg(e.target.value)} rows={6} maxLength={10000} className="w-full mt-1 rounded border border-slate-300 dark:border-slate-700 bg-transparent p-2" placeholder="Paste an email or SMS…" />
      <p className="text-xs text-slate-500">{msg.length} / 10,000 · Rendered as plain text. Links are never opened.</p>
      <div className="grid sm:grid-cols-3 gap-3 mt-3">
        <input aria-label="Sender (optional)" value={sender} onChange={e => setSender(e.target.value)} placeholder="Sender (optional)" className="rounded border border-slate-300 dark:border-slate-700 bg-transparent p-2" />
        <input aria-label="URL (optional)" value={url} onChange={e => setUrl(e.target.value)} placeholder="URL to inspect (optional)" className="rounded border border-slate-300 dark:border-slate-700 bg-transparent p-2" />
        <select aria-label="Message type" value={type} onChange={e => setType(e.target.value)} className="rounded border border-slate-300 dark:border-slate-700 bg-transparent p-2 dark:bg-slate-900"><option value="email">Email</option><option value="sms">SMS</option><option value="other">Other</option></select></div>
      <div className="mt-3 flex gap-2"><button onClick={run} disabled={busy} className="inline-flex items-center gap-2 rounded bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 disabled:opacity-60">{busy && <Loader2 className="animate-spin" size={16} />}{busy ? "Analyzing…" : "Analyze"}</button>
        <button onClick={clear} className="rounded border border-slate-400 px-4 py-2">Clear</button></div>
      {err && <p role="alert" className="mt-3 text-sm text-red-600 dark:text-red-400">{err}</p>}
    </div>);
  const exampleBtns = (<div className="flex flex-wrap gap-2">{examples.map(e => <button key={e.id} onClick={() => load(e)} title={e.why} className="text-xs rounded-full border border-slate-400 px-3 py-1 hover:bg-cyan-50 dark:hover:bg-slate-800">{e.label.replace("Synthetic: ", "")}</button>)}</div>);

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 dark:border-slate-800 bg-slate-900 text-white">
        <div className="max-w-5xl mx-auto px-4 py-3 flex flex-wrap items-center gap-4">
          <span className="flex items-center gap-2 font-bold"><Shield className="text-cyan-400" aria-hidden />ShieldMail AI</span>
          <nav className="flex flex-wrap gap-1 text-sm flex-1">{["Dashboard", "Analyze Message", "Analysis History", "About"].map(p =>
            <button key={p} onClick={() => setPage(p)} aria-current={page === p} className={`px-3 py-1 rounded ${page === p ? "bg-cyan-700" : "hover:bg-slate-800"}`}>{p}</button>)}</nav>
          <button aria-label="Toggle theme" onClick={() => setDark(!dark)}>{dark ? <Sun size={18} /> : <Moon size={18} />}</button></div></header>
      <main className="max-w-5xl mx-auto px-4 py-8 space-y-6">
        {page === "Dashboard" && <>
          <h1 className="text-3xl font-bold">Don't Trust the Message. Verify the Evidence.</h1>
          <p className="text-slate-600 dark:text-slate-400">Paste a suspicious email or SMS. ShieldMail AI lists the warning signs it found, explains why they matter, and is honest about what it cannot know.</p>
          {form}<div><p className="text-sm font-medium mb-2">Quick-start synthetic examples</p>{exampleBtns}</div>
          <div className="grid grid-cols-3 gap-3 text-center">{[["Analyses this session", stats.n], ["High/Critical", stats.high], ["Average score", stats.avg]].map(([k, v]) => <div key={k} className={card}><p className="text-2xl font-bold">{v}</p><p className="text-xs text-slate-500">{k}</p></div>)}</div>
          <div><h2 className="font-semibold mb-2">Recent analyses</h2>{hist.slice(0, 3).map(h => <p key={h.id} className="text-sm">{h.at} — {h.result.risk_level} ({h.result.risk_score})</p>)}{!hist.length && <p className="text-sm text-slate-500">Nothing yet.</p>}</div></>}
        {page === "Analyze Message" && <>{form}{exampleBtns}{res && <ResultView r={res} />}</>}
        {page === "Analysis History" && <>
          <div className="flex justify-between items-center"><h1 className="text-2xl font-bold">Analysis History</h1>{hist.length > 0 && <button onClick={() => setHist([])} className="text-sm underline">Clear all</button>}</div>
          <p className="text-xs text-slate-500">Stored in this browser tab only. Raw message text is never saved.</p>
          {!hist.length && <p>No analyses yet.</p>}
          {hist.map(h => <div key={h.id} className={`${card} flex justify-between items-center`}>
            <button className="text-left" onClick={() => { setRes(h.result); setPage("Analyze Message"); }}><b>{h.result.risk_level} — {h.result.risk_score}/100</b><br /><span className="text-xs text-slate-500">{h.at} · {h.type} · {h.result.verdict}</span></button>
            <button aria-label="Delete entry" onClick={() => setHist(hist.filter(x => x.id !== h.id))}><Trash2 size={16} /></button></div>)}</>}
        {page === "About" && <div className={`${card} space-y-2 text-sm`}><h1 className="text-2xl font-bold">About</h1>
          <p>ShieldMail AI uses deterministic, rule-based checks and a documented additive score. Indicators are evidence, not proof, and the score is not a probability of fraud.</p>
          <p>No link is ever opened, and no domain reputation, WHOIS, DNS or SSL check is performed. No AI model is used in this version. Messages are sent only to your own local backend.</p>
          <p>This is an assistive tool, not a guarantee of scam detection. When in doubt, contact the organization using details you found independently.</p></div>}
      </main></div>);
}
