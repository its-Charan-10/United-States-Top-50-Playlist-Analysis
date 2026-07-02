from fastapi import APIRouter, Depends, HTTPException, Request
from ..middleware.auth import verify_token
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
router = APIRouter()

@router.post("/checkout")
async def create_checkout_session(plan_id: str, user=Depends(verify_token)):
    try:
        # Map plan_id to Stripe Price IDs
        price_map = {
            "basic": "price_...",
            "standard": "price_...",
            "premium": "price_..."
        }
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=user['email'],
            line_items=[{
                'price': price_map.get(plan_id),
                'quantity': 1,
            }],
            mode='subscription',
            success_url=os.getenv("FRONTEND_URL", "http://localhost:3000") + "/success",
            cancel_url=os.getenv("FRONTEND_URL", "http://localhost:3000") + "/profile",
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        return {"error": str(e)}

    # Handle the event (e.g., checkout.session.completed)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Update user plan in Firestore here
        
    return {"status": "success"}
