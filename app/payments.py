import uuid
import logging

logger = logging.getLogger("payment-api")
logging.basicConfig(level=logging.INFO)


def mask_card(card_number: str) -> str:
    return "*" * (len(card_number) - 4) + card_number[-4:]


def luhn_check(card_number: str) -> bool:
    if not card_number.isdigit():
        return False

    digits = [int(digit) for digit in card_number]
    checksum = 0

    for index, digit in enumerate(reversed(digits)):
        if index % 2 == 1:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        checksum += digit

    return checksum % 10 == 0


def tokenize_card(card_number: str) -> str:
    return "tok_" + uuid.uuid4().hex


def imitate_payment_processor(card_token: str, amount: float) -> dict:
    return {
        "status": "approved",
        "transaction_id": "txn_" + uuid.uuid4().hex,
        "amount": amount
    }


def process_payment(card_number: str, amount: float) -> dict:
    if not luhn_check(card_number):
        raise ValueError("Invalid card number")

    masked_card = mask_card(card_number)

    logger.info(f"Processing payment: card={masked_card}, amount={amount}")

    card_token = tokenize_card(card_number)

    processor_result = imitate_payment_processor(card_token, amount)

    return {
        "status": processor_result["status"],
        "transaction_id": processor_result["transaction_id"],
        "card_token": card_token
    }