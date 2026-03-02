import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    stripe_secret_key: str
    stripe_webhook_secret: str


def get_settings() -> Settings:
    secret_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()

    if not secret_key:
        raise RuntimeError("Missing STRIPE_SECRET_KEY")
    if not webhook_secret:
        raise RuntimeError("Missing STRIPE_WEBHOOK_SECRET")

    return Settings(
        stripe_secret_key=secret_key,
        stripe_webhook_secret=webhook_secret,
    )