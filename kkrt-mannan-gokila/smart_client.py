# ═══════════════════════════════════════════════
#  smart_client.py — Angel One SmartAPI client
#  Live LTP / candles / indicators-ku broker API bridge.
#
#  Setup:
#    pip install smartapi-python pyotp
#    Render Environment-la add pannunga:
#      SMART_API_KEY, SMART_CLIENT_ID, SMART_PASSWORD, SMART_TOTP_SECRET
#
#  Credentials illa-na intha module silent-a skip agum —
#  terminal Chartink webhook data-oda mattum work agum.
# ═══════════════════════════════════════════════
import os

SMART_API_KEY     = os.environ.get("SMART_API_KEY", "")
SMART_CLIENT_ID   = os.environ.get("SMART_CLIENT_ID", "")
SMART_PASSWORD    = os.environ.get("SMART_PASSWORD", "")
SMART_TOTP_SECRET = os.environ.get("SMART_TOTP_SECRET", "")

_session = None


def is_configured() -> bool:
    return all([SMART_API_KEY, SMART_CLIENT_ID, SMART_PASSWORD, SMART_TOTP_SECRET])


def login():
    """SmartAPI login — credentials set aana mattum."""
    global _session
    if not is_configured():
        print("[SmartAPI] credentials not set — running without broker data")
        return None
    try:
        from SmartApi import SmartConnect
        import pyotp
        sc = SmartConnect(api_key=SMART_API_KEY)
        totp = pyotp.TOTP(SMART_TOTP_SECRET).now()
        data = sc.generateSession(SMART_CLIENT_ID, SMART_PASSWORD, totp)
        if data.get("status"):
            _session = sc
            print("[SmartAPI] login ✅")
            return sc
        print("[SmartAPI] login failed:", data.get("message"))
    except Exception as e:
        print("[SmartAPI] error:", e)
    return None


def get_ltp(exchange: str, symbol: str, token: str):
    """Live LTP fetch. Example: get_ltp('NSE', 'SBIN-EQ', '3045')"""
    if _session is None:
        return None
    try:
        d = _session.ltpData(exchange, symbol, token)
        return d.get("data", {}).get("ltp")
    except Exception as e:
        print("[SmartAPI] ltp error:", e)
        return None
