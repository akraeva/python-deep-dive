# Stepick.org — Углублённый Python
# 3. Утиная типизация и контракты в Python


from typing import Protocol, runtime_checkable
import random

# 3.3 typing.Protocol


@runtime_checkable
class PaymentProtocol(Protocol):
    transaction_id: int

    def process_payment(self, amount: float) -> str: ...


class CreditCard:
    def __init__(self):
        self.transaction_id = random.randint(1000, 9999)

    def process_payment(self, amount: float) -> str:
        return "Оплата успешно проведена."


class PayPal:
    def __init__(self):
        self.transaction_id = random.randint(1000, 9999)

    def process_payment(self, amount: float) -> str:
        return "Оплата успешно проведена."


def process_transaction(payment: PaymentProtocol, sum: float):
    if isinstance(payment, PaymentProtocol):
        result = payment.process_payment(sum)
        print(result)
        print(payment.transaction_id)
