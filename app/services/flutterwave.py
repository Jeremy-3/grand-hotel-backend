import hmac
import httpx
from app.core.config import settings
from app.utils.logger import logger


def get_headers() -> dict:
    """
    Headers used when communicating with Flutterwave.
    """

    return {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def initiate_payment(
    reservation_id: int,
    payment_id: int,
    amount: int,
    currency: str,
    email: str,
    phone: str,
    name: str,
    tx_ref: str,
) -> dict:
    """
    Create a Flutterwave hosted payment link.

    The payment record should already exist in the database
    with status='pending'.
    """

    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    payload = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": currency,
        "redirect_url": settings.FLW_REDIRECT_URL,
        "customer": {
            "email": email,
            "phone_number": phone,
            "name": name,
        },
        "customizations": {
            "title": "Grand Hotel Payment",
            "description": (
                f"Payment for Grand Hotel reservation " f"{reservation_id}"
            ),
        },
        "meta": {
            "reservation_id": reservation_id,
            "payment_id": payment_id,
            "payment_type": "deposit",
        },
    }

    logger.info("=" * 60)
    logger.info("GRAND HOTEL — FLUTTERWAVE PAYMENT")
    logger.info(f"  Reservation ID: {reservation_id}")
    logger.info(f"  Payment ID:     {payment_id}")
    logger.info(f"  TX Ref:         {tx_ref}")
    logger.info(f"  Amount:         {amount} {currency}")
    logger.info(f"  Email:          {email}")
    logger.info("=" * 60)

    response = httpx.post(
        f"{settings.FLW_BASE_URL}/payments",
        json=payload,
        headers=get_headers(),
        timeout=30,
    )

    logger.info(f"Flutterwave response: " f"{response.status_code} — {response.text}")

    response.raise_for_status()

    data = response.json()

    return {
        "payment_link": data["data"]["link"],
        "tx_ref": tx_ref,
        "raw_response": data,
    }


def verify_transaction(transaction_id: str) -> dict:
    """
    Verify a Flutterwave transaction.

    Never mark a payment as paid simply because the customer
    returned to the redirect URL. Verify the transaction first.
    """

    logger.info(f"Verifying Flutterwave transaction: {transaction_id}")

    response = httpx.get(
        f"{settings.FLW_BASE_URL}/transactions/" f"{transaction_id}/verify",
        headers=get_headers(),
        timeout=30,
    )

    logger.info(
        f"Flutterwave verify response: " f"{response.status_code} — {response.text}"
    )

    response.raise_for_status()

    data = response.json()

    return data["data"]


def verify_webhook_signature(
    payload: bytes,
    signature: str,
) -> bool:
    """
    Verify that a Flutterwave webhook request came from
    Flutterwave.

    Flutterwave's verification mechanism should be configured
    according to the webhook signature/header used by the
    version of the Flutterwave API you are integrating with.
    """

    if not signature:
        return False

    expected = settings.FLW_SECRET_KEY

    return hmac.compare_digest(
        signature,
        expected,
    )
