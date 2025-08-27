import pytest
from module_3 import PaymentProtocol, CreditCard, PayPal


def test_payment_protocol():
    assert isinstance(CreditCard(), PaymentProtocol)
    assert isinstance(PayPal(), PaymentProtocol)
