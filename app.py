# ═══════════════════════════════════════════════
#  app.py — KRT AI Terminal 2.2 (Flask main)
#  Modules: scanner.py · notify.py · ai_engine.py
#           news.py · options.py · smart_client.py
# ═══════════════════════════════════════════════
import os
from flask import Flask, request, jsonify, render_template

from scanner import store, handle_chartink
from notify import send_telegram
from news import get_news
from options import get_option_chain

app = Flask(__name__)


# ═══ UI ═══
@app.route("/")
def index():
    return render_template("index.html")


# ═══ Chartink webhook receiver ═══
@app.route("/webhook/chartink", methods=["POST"])
def chartink_webhook():
    b = request.get_json(silent=True) or request.form.to_dict() or {}
    received = handle_chartink(b)
    return jsonify(ok=True, received=received)


# ═══ API — frontend 45s-ku oru dhadava pull pannum ═══
@app.route("/api/gainers")
def api_gainers():
    return jsonify(store["gainers"])


@app.route("/api/losers")
def api_losers():
    return jsonify(store["losers"])


@app.route("/api/breaks/pd")
def api_pd():
    return jsonify(store["pd"])


@app.route("/api/breaks/pw")
def api_pw():
    return jsonify(store["pw"])


@app.route("/api/breaks/pm")
def api_pm():
    return jsonify(store["pm"])


@app.route("/api/jackpot")
def api_jackpot():
    return jsonify(newSignal=False, jackpots=store["jackpots"])


@app.route("/api/alerts")
def api_alerts():
    return jsonify(store["alerts"])


@app.route("/api/news")
def api_news():
    return jsonify(get_news())


@app.route("/api/oc")
def api_oc():
    return jsonify(get_option_chain())


@app.route("/api/health")
def api_health():
    return jsonify(ok=True, tg=bool(os.environ.get("TG_TOKEN") and os.environ.get("TG_CHAT")))


# ═══ Manual test: /test/telegram open pannina test msg varum ═══
@app.route("/test/telegram")
def test_telegram():
    sent = send_telegram("✅ KRT backend test — Telegram connected!")
    return jsonify(sent=sent)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
