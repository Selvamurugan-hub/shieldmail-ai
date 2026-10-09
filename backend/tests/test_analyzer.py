import pytest
from app.analyzer import analyze
from app.examples import EXAMPLES

@pytest.mark.parametrize("ex", EXAMPLES, ids=[e["id"] for e in EXAMPLES])
def test_examples(ex):
    r = analyze(ex["message"], ex["sender"])
    assert r["risk_level"] in ex["expected_levels"]
    assert set(ex["expected_rules"]) <= {f["rule_id"] for f in r["findings"]}

def test_otp_detected(): assert any(f["rule_id"] == "CRED_REQUEST" for f in analyze("Please share your OTP now")["findings"])
def test_negated_advice_not_flagged(): assert analyze("Never share your OTP with anyone.")["risk_score"] == 0
def test_urgent_word_alone_not_critical(): assert analyze("Urgent: lunch is at noon")["risk_level"] == "Low"
def test_ip_url_is_weak_alone():
    r = analyze("see http://192.168.1.5/x"); assert r["risk_level"] == "Low" and r["findings"]
def test_userinfo_url(): assert any(f["rule_id"] == "URL_USERINFO" for f in analyze("go to http://paypal.com@evil.example/")["findings"])
def test_malformed_url_no_crash(): analyze("visit http://[bad/url now")
def test_shortener_weak(): assert analyze("http://bit.ly/abc")["risk_level"] == "Low"
def test_inconclusive_for_ambiguous(): assert "Inconclusive" in analyze(EXAMPLES[6]["message"])["verdict"]
def test_benign_not_inconclusive(): assert "No warning signs" in analyze("Lunch at noon.")["verdict"]
def test_score_bounds_and_determinism():
    m = EXAMPLES[0]["message"]; a, b = analyze(m, EXAMPLES[0]["sender"]), analyze(m, EXAMPLES[0]["sender"])
    assert 0 <= a["risk_score"] <= 100 and a["risk_score"] == b["risk_score"]
def test_no_model_claimed():
    r = analyze("hello"); assert r["analysis_mode"] == "Rule-based" and r["model_status"]["used"] is False
