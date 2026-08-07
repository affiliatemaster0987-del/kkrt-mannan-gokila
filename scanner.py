# ═══════════════════════════════════════════════
#  scanner.py — Chartink webhook parser + data store
#  Scanner name keyword vachu route pannum:
#    "gainer"        -> gainers
#    "loser"         -> losers
#    "pdh"/"pdl"     -> prev day break calls
#    "pwh"/"week"    -> prev week break calls
#    "pmh"/"month"   -> prev month break calls
#    "jackpot"       -> jackpots (Telegram auto-send)
# ═══════════════════════════════════════════════
from datetime import datetime
from zoneinfo import ZoneInfo

from ai_engine import mk_call, mk_jackpot
from notify import send_many_async, jackpot_msg

# In-memory store (server restart aana clear agum — intraday OK)
store = {
    "gainers": [], "losers": [],
    "pd": [], "pw": [], "pm": [],
    "jackpots": [],
    "alerts": [],
    "last_jackpot_key": "",
}


def _now_ist():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S")


def parse_chartink_payload(b: dict):
    """Chartink webhook body-la irundhu stocks, prices, scan name extract."""
    stocks = [s.strip() for s in str(b.get("stocks", "")).split(",") if s.strip()]
    prices = []
    for p in str(b.get("trigger_prices", "")).split(","):
        try:
            prices.append(float(p.strip()))
        except ValueError:
            prices.append(0.0)
    scan = str(b.get("scan_name") or b.get("alert_name") or "").lower()
    at = b.get("triggered_at") or _now_ist()
    rows = []
    for i, sym in enumerate(stocks):
        ltp = prices[i] if i < len(prices) else 0.0
        rows.append((sym, ltp))
    return rows, scan, at


def handle_chartink(b: dict) -> int:
    """Webhook data-va store-la podum; jackpot-na Telegram auto-send."""
    rows, scan, at = parse_chartink_payload(b)
    print(f'[Chartink] "{scan}" -> {", ".join(s for s, _ in rows)}')

    store["alerts"].insert(0, {"scan": scan, "stocks": [s for s, _ in rows], "at": at})
    store["alerts"] = store["alerts"][:50]

    if "gainer" in scan:
        store["gainers"] = [[sym, ltp, 0, "-"] for sym, ltp in rows]
    elif "loser" in scan:
        store["losers"] = [[sym, ltp, 0, "-"] for sym, ltp in rows]
    elif "pdh" in scan or "pdl" in scan or "prev day" in scan:
        direction = "dn" if ("pdl" in scan or "breakdown" in scan) else "up"
        store["pd"] = [mk_call(sym, ltp, direction, f"PDH/PDL {ltp}") for sym, ltp in rows]
    elif "pwh" in scan or "week" in scan:
        store["pw"] = [mk_call(sym, ltp, "up", f"PWH {ltp}") for sym, ltp in rows]
    elif "pmh" in scan or "month" in scan:
        store["pm"] = [mk_call(sym, ltp, "up", f"PMH {ltp}") for sym, ltp in rows]
    elif "jackpot" in scan:
        store["jackpots"] = [mk_jackpot(sym, ltp) for sym, ltp in rows[:4]]
        key = "|".join(j["sym"] for j in store["jackpots"]) + "|" + str(at)
        if key != store["last_jackpot_key"]:
            store["last_jackpot_key"] = key
            send_many_async([jackpot_msg(j) for j in store["jackpots"]])

    return len(rows)
