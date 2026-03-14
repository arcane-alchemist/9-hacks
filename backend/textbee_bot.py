import os
import httpx
from fastapi import APIRouter, Request, BackgroundTasks

# Create an isolated router just for Textbee webhooks
textbee_router = APIRouter()

# These will be loaded from your .env file
TEXTBEE_API_KEY = os.getenv("TEXTBEE_API_KEY")
TEXTBEE_DEVICE_ID = os.getenv("TEXTBEE_DEVICE_ID")

async def send_sms(phone_number: str, message: str):
    """Hits the Textbee API to send a standard SMS back through your Android device."""
    if not TEXTBEE_API_KEY or not TEXTBEE_DEVICE_ID:
        print("?? Cannot send SMS: Textbee credentials missing from .env")
        return

    url = f"https://api.textbee.dev/api/v1/gateway/devices/{TEXTBEE_DEVICE_ID}/send-sms"
    headers = {
        "x-api-key": TEXTBEE_API_KEY
    }
    payload = {
        "recipients": [phone_number],
        "smsBody": message
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"v SMS Reply dispatched to {phone_number}")
            else:
                print(f"? Textbee API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"? Failed to send SMS via Textbee: {str(e)}")

async def process_and_reply(phone_number: str, message_text: str):
    """Acts as a bridge. Forwards the SMS to our existing AI logic, gets the answer, sends it back."""
    print(f"?? Processing incoming SMS from {phone_number}...\n-> Content: {message_text}", flush=True)
    
    # 1. Forward the query to our own local LegalSaathi core endpoint to prevent duplicated code!
    async with httpx.AsyncClient(timeout=45.0) as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/query", 
                json={"text": message_text, "situation_type": "legal advice"}
            )
            if response.status_code == 200:
                data = response.json()
                reply_text = data.get("response", "I could not generate a response.")
                
                # Note: SMS has a character limit typically. Textbee will stitch large SMS messages via your carrier 
                # automatically, but you might want to slice it if the AI is super verbose.
                
            else:
                reply_text = "Sorry, I am facing temporary technical difficulties."
        except Exception as e:
            reply_text = "System is currently unreachable."
            print(f"Internal routing error: {str(e)}")

    # 2. Fire the SMS back to Textbee
    await send_sms(phone_number, reply_text)

@textbee_router.post("/textbee/webhook")
async def textbee_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    This endpoint is invoked by Textbee whenever your Android phone receives a new SMS message.
    """
    try:
        payload = await request.json()
        print(f"Received Webhook Payload: {payload}", flush=True)
        
        # Depending on how the user configured Textbee, it passes properties identifying the sender and message
        # We check common webhook properties 
        phone_number = payload.get("sender") or payload.get("from")
        message_text = payload.get("body") or payload.get("message") or payload.get("text")

        if phone_number and message_text:
            # We add to background tasks so we immediately return '200 OK' to Textbee. 
            # If we don't, Textbee might think the webhook failed while waiting for the LLM to generate an answer.
            background_tasks.add_task(process_and_reply, phone_number, message_text)
            return {"status": "success", "message": "Textbee Webhook received & processing started"}
        
        return {"status": "ignored", "message": "Payload didn't contain required fields"}
    except Exception as e:
        print(f"Webhook processing error: {e}")
        return {"status": "error", "message": str(e)}



