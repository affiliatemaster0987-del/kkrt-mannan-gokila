# ═══════════════════════════════════════════════
#  notify.py — Telegram / WhatsApp alert sender
# ═══════════════════════════════════════════════
import os
import time
import threading
import requests

TG_TOKEN = os.environ.get("TG_TOKEN", "")   # @BotFather token
TG_CHAT  = os.environ.get("TG_CHAT", "")    # @userinfobot chat id


def send_telegram(text: str) -> bool:
    """Oru message-a Telegram-ku anuppum."""
    if not TG_TOKEN or not TG_CHAT:
        print("[TG] token/chat not set — skipping")
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT, "text": text},
            timeout=10,
        )
        d = r.json()
        ok = bool(d.get("ok"))
        print("[TG]", "sent ✅" if ok else "failed: " + str(d.get("description")))
        return ok
    except Exception as e:
        print("[TG] error", e)
        return False


def send_many_async(messages):
    """List of messages-a background thread-la anuppum (webhook delay aagadhu)."""
    def worker():
        for m in messages:
            send_telegram(m)
            time.sleep(0.7)
    threading.Thread(target=worker, daemon=True).start()


def jackpot_msg(j: dict) -> str:
    """Jackpot dict-a Telegram message format-ku maathum."""
    return (
        f"🚀 KRT AI JACKPOT\n\n"
        f"Stock : {j['sym']}\n"
        f"AI Score : {j['score']}/100\n"
        f"Probability : {j['prob']}%\n"
        f"Filters : {j['pass']}/{j['tot']} ✅\n\n"
        f"🟢 BUY\nEntry: {j['e']}\nSL: {j['sl']}\n"
        f"T1: {j['t1']} | T2: {j['t2']} | T3: {j['t3']}\n\n"
        f"{j['why']}\n\n"
        f"⚠ Educational only. Not investment advice."
    )
