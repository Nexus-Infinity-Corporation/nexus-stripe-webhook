from __future__ import annotations

from typing import Any, Dict

import stripe

from app.domain.events import StripeEvent, to_domain_event


class StripeWebhookService:
    """
    - Verifies Stripe signature
    - Converts raw Stripe event to a small domain object
    - Dispatches to handlers
    """

    def __init__(self, stripe_secret_key: str, webhook_secret: str) -> None:
        stripe.api_key = stripe_secret_key
        self._webhook_secret = webhook_secret

    def verify_and_parse_event(self, payload: bytes, stripe_signature: str | None) -> StripeEvent:
        if not stripe_signature:
            raise ValueError("Missing Stripe-Signature header")

        try:
            evt = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=stripe_signature,
                secret=self._webhook_secret,
            )
        except stripe.error.SignatureVerificationError as e:
            raise ValueError("Invalid Stripe signature") from e
        except Exception as e:
            raise ValueError("Invalid webhook payload") from e

        # stripe.Event is dict-like; convert to plain dict for our domain
        raw: Dict[str, Any] = dict(evt)
        return to_domain_event(raw)

    def handle_event(self, event: StripeEvent) -> None:
        # Minimal dispatch
        if event.type == "checkout.session.completed":
            self._on_checkout_session_completed(event)
            return

        if event.type == "payment_intent.succeeded":
            self._on_payment_intent_succeeded(event)
            return

        if event.type == "payment_intent.payment_failed":
            self._on_payment_intent_failed(event)
            return

        # Unhandled event types should still return 2xx to Stripe
        # so you don’t get retries for irrelevant events.

    def _on_checkout_session_completed(self, event: StripeEvent) -> None:
        session_id = event.data_object.get("id")
        customer = event.data_object.get("customer")
        print(f"[stripe] checkout.session.completed session_id={session_id} customer={customer}")

    def _on_payment_intent_succeeded(self, event: StripeEvent) -> None:
        pi_id = event.data_object.get("id")
        amount = event.data_object.get("amount_received")
        currency = event.data_object.get("currency")
        print(f"[stripe] payment_intent.succeeded id={pi_id} amount={amount} {currency}")

    def _on_payment_intent_failed(self, event: StripeEvent) -> None:
        pi_id = event.data_object.get("id")
        last_error = (event.data_object.get("last_payment_error") or {}).get("message")
        print(f"[stripe] payment_intent.payment_failed id={pi_id} error={last_error}")