from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from app.auth import verify_token, create_demo_token
from app.payments import process_payment
from app.crypto import encrypt_value

app = FastAPI(title="Secure Payment API")


class PaymentRequest(BaseModel):
    card_number: str
    cvv: str
    amount: float


@app.get("/")
def root():
    return {"message": "Secure Payment API is running"}


@app.get("/demo-token")
def demo_token():
    return {"access_token": create_demo_token()}


@app.post("/payments")
def create_payment(request: PaymentRequest, user=Depends(verify_token)):
    try:
        payment_result = process_payment(request.card_number, request.amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid card number")

    encrypted_token = encrypt_value(payment_result["card_token"])

    return {
        "status": payment_result["status"],
        "transaction_id": payment_result["transaction_id"],
        "encrypted_card_token": encrypted_token
    }