from enum import Enum


class PaymentOptionType(str, Enum):
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    CARD_PAYMENT = "CARD_PAYMENT"
    ON_DELIVERY = "ON_DELIVERY"
    PREPAYMENT_100 = "PREPAYMENT_100"
