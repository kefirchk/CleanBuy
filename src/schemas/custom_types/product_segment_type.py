from enum import Enum


class ProductSegmentType(str, Enum):
    LUXURY = "LUXURY"
    PREMIUM = "PREMIUM"
    NICHE = "NICHE"
    MASS_MARKET = "MASS MARKET"
    BUDGET = "BUDGET"
    SEASONAL = "SEASONAL"
    ALL = "ALL"
