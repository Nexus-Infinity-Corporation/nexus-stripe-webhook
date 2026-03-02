from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

StripeEventType = Literal[
    "checkout.session.completed",
    "payment_intent.succeeded",
    "payment_intent.payment_failed",
]


@dataclass(frozen=True)
class StripeEvent:
    id: str
    type: str
    data_object: Dict[str, Any]


def to_domain_event(raw_event: Dict[str, Any]) -> StripeEvent:
    return StripeEvent(
        id=str(raw_event.get("id", "")),
        type=str(raw_event.get("type", "")),
        data_object=(raw_event.get("data", {}) or {}).get("object", {}) or {},
    )