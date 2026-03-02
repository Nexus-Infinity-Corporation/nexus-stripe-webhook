# crm-nexus-stripe

A lightweight FastAPI service that receives and processes Stripe webhook events for the Nexus Infinity CRM.

## Features

- Verifies Stripe webhook signatures
- Handles `checkout.session.completed`, `payment_intent.succeeded`, and `payment_intent.payment_failed` events
- Health check endpoint

## Project Structure

```
app/
├── api/
│   ├── healt_check.py       # GET /health
│   └── stripe_webhooks.py   # POST /stripe/webhook
├── core/
│   └── config.py            # Settings from environment variables
├── domain/
│   └── events.py            # StripeEvent domain model
├── services/
│   └── stripe_webhooks.py   # Signature verification & event handling
└── main.py                  # FastAPI app entry point
```

## Environment Variables

| Variable | Description |
|---|---|
| `STRIPE_SECRET_KEY` | Stripe secret API key |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret from the Stripe dashboard |

Copy `.env.example` to `.env` and fill in the values.

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or with Gunicorn for production:

```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/stripe/webhook` | Stripe webhook receiver |
