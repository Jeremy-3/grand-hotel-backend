import base64
from datetime import datetime
import httpx
from app.core.config import settings
from app.utils.logger import logger


def normalize_phone(phone: str) -> str:
    """
    Convert Kenyan phone numbers to 254XXXXXXXXX format.

    Examples:
        0712345678  -> 254712345678
        +254712345678 -> 254712345678
        254712345678 -> 254712345678
    """

    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+"):
        phone = phone[1:]

    if phone.startswith("0"):
        phone = "254" + phone[1:]

    if not phone.startswith("254"):
        raise ValueError("Invalid Kenyan phone number.")

    if len(phone) != 12:
        raise ValueError("Invalid Kenyan phone number.")

    return phone


def get_access_token() -> str:
    """
    Get an OAuth access token from Safaricom.
    """

    credentials = base64.b64encode(
        f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
    ).decode()

    url = (
        f"{settings.MPESA_BASE_URL}" "/oauth/v1/generate?grant_type=client_credentials"
    )

    logger.info(f"Requesting M-Pesa access token from {settings.MPESA_BASE_URL}")

    response = httpx.get(
        url,
        headers={"Authorization": f"Basic {credentials}"},
        timeout=30,
    )

    logger.info(f"Token response: {response.status_code} — {response.text}")

    response.raise_for_status()

    return response.json()["access_token"]


def get_password() -> tuple[str, str]:
    """
    Generate the M-Pesa STK Push password and timestamp.
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    raw = f"{settings.MPESA_SHORTCODE}" f"{settings.MPESA_PASSKEY}" f"{timestamp}"

    password = base64.b64encode(raw.encode()).decode()

    return password, timestamp


def stk_push(
    phone: str,
    amount: int,
    reservation_id: int,
    payment_id: int,
    description: str = "Grand Hotel reservation deposit",
) -> dict:
    """
    Initiate an M-Pesa STK Push for a hotel reservation payment.

    The payment itself should already exist in the database with
    status='pending' before this function is called.
    """

    phone = normalize_phone(phone)

    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    token = get_access_token()
    password, timestamp = get_password()

    account_reference = f"GH-RES-{reservation_id}"

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": description[:20],
    }

    url = f"{settings.MPESA_BASE_URL}" "/mpesa/stkpush/v1/processrequest"

    logger.info("=" * 60)
    logger.info("GRAND HOTEL — M-PESA STK PUSH")
    logger.info(f"  Reservation ID: {reservation_id}")
    logger.info(f"  Payment ID:     {payment_id}")
    logger.info(f"  Amount:         {amount}")
    logger.info(f"  Phone:          {phone}")
    logger.info(f"  Account Ref:    {account_reference}")
    logger.info(f"  Callback URL:   {settings.MPESA_CALLBACK_URL}")
    logger.info(f"  Environment:    {settings.MPESA_ENV}")
    logger.info("=" * 60)

    response = httpx.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    logger.info("M-PESA STK PUSH RESPONSE")
    logger.info(f"  Status: {response.status_code}")
    logger.info(f"  Body:   {response.text}")
    logger.info("=" * 60)

    response.raise_for_status()

    data = response.json()

    return {
        "merchant_request_id": data.get("MerchantRequestID"),
        "checkout_request_id": data.get("CheckoutRequestID"),
        "response_code": data.get("ResponseCode"),
        "response_description": data.get("ResponseDescription"),
        "customer_message": data.get("CustomerMessage"),
        "raw_response": data,
    }


def query_stk_status(checkout_request_id: str) -> dict:
    """
    Query the status of an M-Pesa STK Push.
    """

    token = get_access_token()
    password, timestamp = get_password()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }

    url = f"{settings.MPESA_BASE_URL}" "/mpesa/stkpushquery/v1/query"

    logger.info(f"Querying M-Pesa STK status: {checkout_request_id}")

    response = httpx.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    logger.info(f"STK status response: " f"{response.status_code} — {response.text}")

    response.raise_for_status()

    return response.json()
