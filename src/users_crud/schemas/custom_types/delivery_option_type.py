from enum import Enum


class DeliveryOptionType(str, Enum):
    INCLUDED = "INCLUDED"
    NOT_INCLUDED = "NOT_INCLUDED"
    NEGOTIABLE = "NEGOTIABLE"
