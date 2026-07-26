from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TAX_AND_FEE_RATE = Decimal("0.10")
WHOLE_YEN = Decimal("1")


@dataclass(frozen=True)
class BookingPrice:
    base_fare: Decimal
    taxes_and_fees: Decimal
    total_price: Decimal


def calculate_booking_price(base_fare):
    base_fare = Decimal(base_fare).quantize(WHOLE_YEN, rounding=ROUND_HALF_UP)
    taxes_and_fees = (base_fare * TAX_AND_FEE_RATE).quantize(WHOLE_YEN, rounding=ROUND_HALF_UP)
    return BookingPrice(
        base_fare=base_fare,
        taxes_and_fees=taxes_and_fees,
        total_price=base_fare + taxes_and_fees,
    )
