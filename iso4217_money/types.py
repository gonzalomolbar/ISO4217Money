from __future__ import annotations

from decimal import Decimal
from typing import TypedDict, Union


class ISO4217Currency(TypedDict):
    entity: str
    alphabetic_code: str
    numeric_code: str
    minor_unit: str
    country_names: set[str]


AmountTypeAllowed = (str, int, float, Decimal)
AmountTypeAllowedHint = Union[str, int, float, Decimal]
