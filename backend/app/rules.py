"""Rule-based detectors. Each returns a list of finding dicts. No network access, ever."""
import ipaddress, re
from urllib.parse import urlparse
from .config import BRANDS, LOOKALIKES, SHORTENERS

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"']+", re.I)
I = re.I

def _f(rule_id, category, title, desc, severity, evidence, points):
    return dict(rule_id=rule_id, category=category, title=title, description=desc,
                severity=severity, evidence=evidence[:160], points_contributed=points)

def _negated(text, start):
    """True for advice like 'never share your OTP'."""
    return bool(re.search(r"(never|do not|don't|dont|won't|not)\W+(?:\w+\W+){0,3}$", text[max(0, start - 30):start].lower()))

def sender_domain(sender):
    m = re.search(r"@([\w.-]+)", sender or "")
    return m.group(1).lower().rstrip(".") if m else None

def _legit(host, brand):
    return any(host == d or host.endswith("." + d) for d in BRANDS[brand])

def credential(text):
    pat = re.compile(r"\b(send|share|reply with|provide|enter|confirm|tell|give|verify|update)\b[^.\n]{0,40}?\b"
                     r"(password|otp|one[- ]time (?:code|password)|pin|cvv|recovery code|verification code|bank (?:details|account))", I)
    return [_f("CRED_REQUEST", "credential", "Requests sensitive information",
               "The message asks you to hand over a credential or code. Legitimate organizations rarely ask for these by message.",
               "high", m.group(0), 20) for m in pat.finditer(text) if not _negated(text, m.start())][:1]

def urgency(text):
    pat = re.compile(r"(within \d+ ?(?:hours?|minutes?)|account (?:will be )?(?:closed|locked|suspended|terminated)|"
                     r"(?:will be|has been) (?:suspended|locked|terminated)|final notice|last warning|act now|immediately)", I)
    hits = [m for m in pat.finditer(text) if not _negated(text, m.start())]
    if not hits:
        return []
    return [_f("URGENCY_THREAT", "urgency", "Pressure or threat",
               "Artificial deadlines and threats push people to act before verifying.",
               "medium", hits[0].group(0), 15)]

def url_checks(text, extra_url=None, sender=None):
    urls = URL_RE.findall(text) + ([extra_url] if extra_url else [])
    out, seen = [], set()
    for raw in urls:
        raw = raw.rstrip(".,);]")
        if raw in seen:
            continue
        seen.add(raw)
        try:
            p = urlparse(raw if "://" in raw else "http://" + raw)
            host = (p.hostname or "").lower()
        except ValueError:
            out.append(_f("URL_MALFORMED", "url", "Malformed URL", "The link could not be parsed, which can hide its real target.", "low", raw, 8))
            continue
        if not host:
            continue
        try:
            ipaddress.ip_address(host)
            out.append(_f("URL_IP_HOST", "url", "Link uses a raw IP address", "Legitimate services usually use domain names; IP hosts are a weak-to-moderate warning sign.", "medium", raw, 12))
        except ValueError:
            pass
        if p.username is not None or p.password is not None:
            out.append(_f("URL_USERINFO", "url", "Link contains a username/password part", "Text before '@' can make a link look like it points to a trusted site.", "high", raw, 20))
        if host in SHORTENERS:
            out.append(_f("URL_SHORTENER", "url", "Shortened link hides destination", "Shorteners are common and often legitimate, so this is only a weak signal.", "low", raw, 8))
        if host.startswith("xn--") or ".xn--" in host:
            out.append(_f("URL_PUNYCODE", "url", "Internationalized (punycode) domain", "Lookalike characters can disguise a domain.", "medium", raw, 15))
        if any(l in host for l in LOOKALIKES):
            out.append(_f("URL_LOOKALIKE", "url", "Lookalike domain", "The domain imitates a known brand spelling.", "high", raw, 20))
        if host.count(".") >= 4:
            out.append(_f("URL_SUBDOMAINS", "url", "Unusually many subdomains", "Long subdomain chains can bury the real domain.", "low", raw, 10))
        if "%" in (p.netloc or "") :
            out.append(_f("URL_ENCODED_HOST", "url", "Encoded characters in host", "Percent-encoding in the host is unusual.", "medium", raw, 12))
        for b in BRANDS:
            if b in host and not _legit(host, b):
                out.append(_f("URL_BRAND_MISMATCH", "impersonation", "Brand name inside an unrelated domain",
                              f"'{b}' appears in a domain that is not on this brand's configured list. This does not prove the site is fake.",
                              "high", raw, 20))
    return out

def impersonation(text, sender):
    dom = sender_domain(sender)
    out = []
    for b in BRANDS:
        claim = re.search(rf"(?:from\s+{b}\b|\b{b}\s+(?:team|support|security|customer|account|billing)\b)", text, I)
        if claim and dom and not _legit(dom, b):
            out.append(_f("IMPERSONATION_SENDER_MISMATCH", "impersonation", "Claimed organization does not match sender domain",
                          f"The message claims to be from {b}, but the sender domain '{dom}' is not one of its configured domains.",
                          "high", claim.group(0), 20))
    return out

def claims_unverified(text, sender):
    return not sender_domain(sender) and any(re.search(rf"\b{b}\b", text, I) for b in BRANDS)

def payment(text):
    pats = [("PAY_GIFTCARD_CRYPTO", r"\b(pay|payment|send|buy|purchase)\b[^.\n]{0,40}?(gift cards?|bitcoin|crypto(?:currency)?|western union)", "Unusual payment method"),
            ("PAY_CHANGED_BANK", r"\b(?:changed|new|updated)\s+(?:(?:our|my|the|your)\s+)?(?:bank|account|payment)\s+(?:details|account|information)", "Changed bank details"),
            ("PAY_URGENT_TRANSFER", r"\b(?:wire|transfer)\b[^.\n]{0,40}?(?:today|immediately|urgent|asap|now)\b", "Urgent transfer request")]
    out = []
    for rid, p, title in pats:
        m = re.search(p, text, I)
        if m:
            out.append(_f(rid, "payment", title, "Payment requests with unusual methods, new accounts, or deadlines are a common fraud pattern; confirm via a second channel.", "high", m.group(0), 20))
    return out

def reward(text):
    m = re.search(r"\b(you(?:'ve| have)? won|winner|congratulations|prize|lottery|unexpected refund)\b", text, I)
    return [_f("REWARD_UNEXPECTED", "reward", "Unexpected prize or refund", "Unsolicited rewards are a common lure.", "medium", m.group(0), 10)] if m else []

def context(text):
    pats = [("CTX_BYPASS_VERIFICATION", r"(keep this confidential|do not (?:tell|call|contact)|don't (?:tell|call|contact)|skip (?:the )?verification)", "Asks to bypass normal verification"),
            ("CTX_ATTACHMENT", r"\b(?:see|open|download)\b[^.\n]{0,20}?attach(?:ed|ment)", "Unexpected attachment mentioned")]
    return [_f(r, "context", t, "A contextual signal that is weak on its own.", "low", m.group(0), 5)
            for r, p, t in pats if (m := re.search(p, text, I))]

def security_context(text):
    return bool(re.search(r"security alert|sign[- ]in|new device|unusual activity|verify your account", text, I))
