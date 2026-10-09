import os
MAX_CHARS = int(os.getenv("SHIELDMAIL_MAX_CHARS", "10000"))
CORS_ORIGINS = [o.strip() for o in os.getenv(
    "SHIELDMAIL_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]
# Brand -> legitimate domains (configurable test data, fictional brand included)
BRANDS = {"paypal": {"paypal.com"}, "microsoft": {"microsoft.com"}, "amazon": {"amazon.com"},
          "apple": {"apple.com"}, "google": {"google.com"}, "examplebank": {"examplebank.example"}}
LOOKALIKES = {"paypa1", "micros0ft", "arnazon", "g00gle", "examp1ebank"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "ow.ly"}
# Category weights (documented in README). Each category counts once.
WEIGHTS = {"credential": 20, "urgency": 15, "url": 20, "impersonation": 20,
           "payment": 20, "reward": 10, "context": 5}
COMBO_BONUS = 10  # added when 3+ distinct categories fire
