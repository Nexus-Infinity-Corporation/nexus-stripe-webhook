from fastapi import APIRouter, Header, HTTPException, Request, status

from app.core.config import get_settings
from app.services.stripe_webhooks import StripeWebhookService

router = APIRouter()


@router.post("/stripe/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
):
    payload = await request.body()

    settings = get_settings()
    service = StripeWebhookService(
        stripe_secret_key=settings.stripe_secret_key,
        webhook_secret=settings.stripe_webhook_secret,
    )

    try:
        event = service.verify_and_parse_event(payload=payload, stripe_signature=stripe_signature)
        service.handle_event(event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"ok": True}