from fastapi import FastAPI

from app.api.healt_check import router as health_router
from app.api.stripe_webhooks import router as webhook_router

app = FastAPI(title="Stripe Webhook Service")

app.include_router(health_router)
app.include_router(webhook_router)