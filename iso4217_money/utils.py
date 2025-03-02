from __future__ import annotations

from decimal import Decimal

from iso4217_money.types import AmountTypeAllowedHint


def normalize_amount(amount_raw: AmountTypeAllowedHint) -> Decimal:
    if isinstance(amount_raw, str):
        return Decimal(amount_raw)
    if isinstance(amount_raw, float):
        return Decimal(str(amount_raw))
    elif isinstance(amount_raw, int):
        return Decimal(amount_raw)
    return amount_raw
