import httpx
from fastapi import HTTPException, status
from core.config import settings

async def send_otp_via_eskiz(code: str, phone_number: str) -> None:

    auth_url = settings.SMS_AUTH_URL      
    sms_url = settings.SMS_SEND_URL       
    username = settings.SMS_USERNAME
    password = settings.SMS_PASSWORD
    sender = settings.SMS_SENDER

    if not (auth_url and sms_url and username and password):
        print(f"[OTP] Eskiz SMS not configured, code for {phone_number}: {code}")
        return

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            auth_resp = await client.post(
                auth_url,
                json={"username": username, "password": password}
            )
            auth_resp.raise_for_status()
            token = auth_resp.json().get("data", {}).get("token")
            if not token:
                raise ValueError("No token in Eskiz response")

            payload = {
                "mobile_phone": phone_number,
                "message": f"Ваш OTP-код: {code}",
                "from": sender
            }
            headers = {"Authorization": f"Bearer {token}"}
            sms_resp = await client.post(sms_url, json=payload, headers=headers)
            sms_resp.raise_for_status()
    except Exception as e:
        print(f"Failed to send OTP via Eskiz: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send OTP via SMS"
        )