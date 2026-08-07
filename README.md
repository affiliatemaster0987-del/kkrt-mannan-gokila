# 🚀 KRT AI Terminal 2.2

Chartink webhook + Telegram jackpot alerts + TradingView live chart terminal.

## Structure
- `app.py` — Flask main (routes)
- `scanner.py` — Chartink webhook parser + data store
- `notify.py` — Telegram / WhatsApp sender
- `ai_engine.py` — Signal builders, 18-filter scoring
- `news.py` — News store (extend for live news AI)
- `options.py` — Option chain store (PCR / Max Pain)
- `smart_client.py` — Angel One SmartAPI bridge (optional, live LTP)
- `templates/index.html` + `static/style.css` + `static/script.js` — UI

## Render Deploy
1. GitHub push → Render New Web Service
2. Build: `pip install -r requirements.txt` · Start: `gunicorn app:app`
3. Environment: `TG_TOKEN` (@BotFather) + `TG_CHAT` (@userinfobot)
4. Test: open `/test/telegram` → Telegram-la msg vandha connected ✅

## Chartink Connect
Scanner → Create Alert → Webhook URL:
`https://YOUR-URL.onrender.com/webhook/chartink`

Scanner NAME-la keyword MUST iruku:
| Keyword | Where it shows |
|---|---|
| gainer | Top Gainers |
| loser | Top Losers |
| pdh / pdl | Prev Day Break calls |
| pwh / week | Prev Week High Break calls |
| pmh / month | Prev Month High Break calls |
| jackpot | 🎰 Jackpots + Telegram AUTO-SEND ✈ |

⚠ Chartink webhooks = paid plan only. Render free plan sleeps in 15 min — use UptimeRobot ping or paid plan.

Educational & personal use only · Not investment advice · SEBI RA registration required for public advisory.
