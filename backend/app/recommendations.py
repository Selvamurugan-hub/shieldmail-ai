REC = {
 "credential": "Never share an OTP, password, PIN, or recovery code. If you already did, change it via the official website and contact the provider.",
 "urgency": "Pressure is a manipulation tactic. Slow down and verify before acting.",
 "url": "Do not click the link. Open the organization's official website by typing its address yourself.",
 "impersonation": "Contact the organization using a phone number or website you obtained independently.",
 "payment": "Verify any payment or bank-detail change through a second, trusted channel before sending money.",
 "reward": "Unexpected prizes that ask for fees or details are a classic lure; do not pay to claim them.",
 "context": "Be cautious with unexpected attachments or requests to skip normal verification.",
}
DEFAULT = ["No strong warning signs found, but that is not a guarantee. If anything feels off, verify independently."]
REPORT = "Report suspicious messages using your email or messaging service's official reporting feature."
def build(categories):
    recs = [REC[c] for c in REC if c in categories]
    return (recs + [REPORT]) if recs else DEFAULT
