import logging
from app.payments import process_payment


def test_card_number_not_in_logs(caplog):
    card_number = "4111111111111111"

    with caplog.at_level(logging.INFO):
        process_payment(card_number, 100)

    logs = caplog.text

    assert card_number not in logs
    assert "************1111" in logs