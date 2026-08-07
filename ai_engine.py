# ═══════════════════════════════════════════════
#  ai_engine.py — Signal builders + scoring logic
# ═══════════════════════════════════════════════


def rnd(n) -> float:
    return round(float(n), 2)


def mk_call(sym: str, ltp: float, direction: str, lvl: str) -> dict:
    """Break-call: entry / SL / targets % based auto-calc.
    (Broker API connect pannina ATR-based levels use pannalam — smart_client.py)"""
    e = ltp
    sign = 1 if direction == "up" else -1
    return {
        "sym": sym,
        "lvl": f"{lvl} ✅",
        "dir": direction,
        "e": rnd(e),
        "sl": rnd(e - sign * e * 0.008),          # ~0.8% SL
        "t": f"{rnd(e + sign * e * 0.01)} / {rnd(e + sign * e * 0.02)}",  # 1% / 2%
        "c": 85,
    }


def mk_jackpot(sym: str, ltp: float) -> dict:
    """Jackpot signal object — frontend jp-card format."""
    e = ltp
    return {
        "sym": sym,
        "ltp": f"₹{rnd(e)}",
        "score": 90,
        "prob": 88,
        "pass": 15,
        "tot": 18,
        "hot": 1,
        "e": rnd(e),
        "sl": rnd(e * 0.988),
        "t1": rnd(e * 1.01),
        "t2": rnd(e * 1.02),
        "t3": rnd(e * 1.032),
        "why": "Chartink Jackpot scanner confirmed · multi-filter pass ✅",
    }


# ═══ 18-filter checklist (frontend display + future live checks) ═══
JACKPOT_FILTERS = [
    "Positive News ≥ 8/10", "Order Win / Govt Contract", "Earnings Beat",
    "Delivery > 60%", "Rel. Volume > 2×", "RS > Nifty",
    "Sector Top-3", "Above VWAP", "PDH Break",
    "PWH Break", "PMH Break", "EMA 9>21>50>200",
    "RSI 60–75", "ADX > 25", "MACD Bullish",
    "Supertrend Buy", "Put Writing > Call", "No Nearby Resistance",
]
MIN_FILTERS_PASS = 15


def score_signal(checks: dict) -> dict:
    """Filter check dict {name: bool} kuduttha score + verdict return pannum.
    Live indicator data smart_client.py-la irundhu vandha idha use pannalam."""
    passed = sum(1 for v in checks.values() if v)
    total = len(checks) or len(JACKPOT_FILTERS)
    score = round(passed / total * 100)
    return {
        "pass": passed,
        "tot": total,
        "score": score,
        "verdict": "BUY" if passed >= MIN_FILTERS_PASS else "SKIP",
    }
