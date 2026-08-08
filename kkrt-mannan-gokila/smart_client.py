# ═══════════════════════════════════════════════
# smart_client.py — Angel One SmartAPI Client
# ═══════════════════════════════════════════════

import os

_session = None

SMARTAPI_KEY = os.getenv("SMARTAPI_KEY", "")
SMARTAPI_CLIENT = os.getenv("SMARTAPI_CLIENT", "")
SMARTAPI_PASSWORD = os.getenv("SMARTAPI_PASSWORD", "")
SMARTAPI_TOTP = os.getenv("SMARTAPI_TOTP", "")


def is_configured():
    return all([
        SMARTAPI_KEY,
        SMARTAPI_CLIENT,
        SMARTAPI_PASSWORD,
        SMARTAPI_TOTP
    ])


def login():
    global _session

    if _session:
        return _session

    if not is_configured():
        print("[SmartAPI] Environment variables missing")
        return None

    try:
        from SmartApi import SmartConnect
        import pyotp

        sc = SmartConnect(api_key=SMARTAPI_KEY)

        otp = pyotp.TOTP(SMARTAPI_TOTP).now()

        data = sc.generateSession(
            SMARTAPI_CLIENT,
            SMARTAPI_PASSWORD,
            otp
        )

        if data.get("status"):
            _session = sc
            print("[SmartAPI] Login Success")
            return sc

        print("[SmartAPI] Login Failed:", data)

    except Exception as e:
        print("[SmartAPI] ERROR:", e)

    return None


def get_ltp(exchange, symbol, token):
    global _session

    if _session is None:
        login()

    if _session is None:
        return None

    try:
        res = _session.ltpData(exchange, symbol, token)

        if res.get("status"):
            return res["data"]["ltp"]

        print("[SmartAPI] LTP Error:", res)

    except Exception as e:
        print("[SmartAPI] LTP Exception:", e)

    return None
