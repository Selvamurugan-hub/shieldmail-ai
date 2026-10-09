import uuid
from . import rules, recommendations
from .config import WEIGHTS, COMBO_BONUS

LIMITS = ["Heuristic indicators are evidence, not proof; the score is not a probability of fraud.",
          "No URL was visited and no domain reputation, WHOIS, DNS, or SSL check was performed.",
          "Sender identity cannot be verified from pasted text alone."]

def level(score):
    return "Low" if score < 25 else "Medium" if score < 50 else "High" if score < 75 else "Critical"

def analyze(message, sender=None, url=None, message_type="email"):
    found = (rules.credential(message) + rules.urgency(message) + rules.url_checks(message, url, sender)
             + rules.impersonation(message, sender) + rules.payment(message) + rules.reward(message) + rules.context(message))
    best = {}
    for f in found:  # one scoring slot per category: the strongest finding carries the points
        f["_pts"], f["points_contributed"] = f["points_contributed"], 0
        if f["category"] not in best or f["_pts"] > best[f["category"]]["_pts"]:
            best[f["category"]] = f
    score = 0
    for cat, f in best.items():
        f["points_contributed"] = min(WEIGHTS[cat], f["_pts"])
        score += f["points_contributed"]
    if len(best) >= 3:
        score += COMBO_BONUS
    score = max(0, min(100, score))
    for f in found:
        f.pop("_pts", None)
    cats = set(best)
    unverified = rules.claims_unverified(message, sender)
    ambiguous = unverified or rules.security_context(message) or bool(rules.URL_RE.search(message))
    if score >= 50 or len(cats) >= 3:
        strength, verdict = "Multiple warning signs", "Multiple warning signs — treat as suspicious"
    elif score >= 25 or len(cats) == 2:
        strength, verdict = "Moderate evidence", "Some suspicious indicators — verify independently"
    elif cats:
        strength, verdict = "Limited evidence", "Inconclusive — verify independently"
    elif ambiguous:
        strength, verdict = "Insufficient evidence", "Inconclusive — verify independently"
    else:
        strength, verdict = "Insufficient evidence", "No warning signs detected (not a guarantee)"
    limits = list(LIMITS) + (["A brand is mentioned but no sender was supplied, so impersonation could not be checked."] if unverified else [])
    return dict(analysis_id=str(uuid.uuid4()), risk_score=score, risk_level=level(score), verdict=verdict,
                evidence_strength=strength, findings=found,
                evidence_snippets=list(dict.fromkeys(f["evidence"] for f in found)),
                recommendations=recommendations.build(cats), analysis_mode="Rule-based", limitations=limits,
                model_status={"used": False, "detail": "No AI model configured; rule-based analysis only."})
