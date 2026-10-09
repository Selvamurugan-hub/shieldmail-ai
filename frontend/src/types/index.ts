export interface Finding { rule_id: string; category: string; title: string; description: string; severity: string; evidence: string; points_contributed: number }
export interface Result { analysis_id: string; risk_score: number; risk_level: "Low"|"Medium"|"High"|"Critical"; verdict: string; evidence_strength: string; findings: Finding[]; evidence_snippets: string[]; recommendations: string[]; analysis_mode: string; limitations: string[]; model_status: { used: boolean; detail: string } }
export interface Example { id: string; label: string; message: string; sender: string | null; message_type: "email"|"sms"|"other"; why: string }
export interface HistoryItem { id: string; at: string; type: string; result: Result }
