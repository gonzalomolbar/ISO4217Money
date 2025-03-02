from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal


@dataclass
class CurrencyFormatting:
    """Class containing all the formatting parameters necessary."""

    thousand_delimiter: str
    decimal_delimiter: str
    symbol_space: bool
    symbol_position: Literal["left", "right"]


AMERICAN_FORMATTING_LEFT = CurrencyFormatting(
    thousand_delimiter=",",
    decimal_delimiter=".",
    symbol_space=False,
    symbol_position="left",
)
AMERICAN_FORMATTING_LEFT_SPACED = CurrencyFormatting(
    thousand_delimiter=",",
    decimal_delimiter=".",
    symbol_space=True,
    symbol_position="left",
)
AMERICAN_FORMATTING_RIGHT_SPACED = CurrencyFormatting(
    thousand_delimiter=",",
    decimal_delimiter=".",
    symbol_space=True,
    symbol_position="right",
)

EUROPEAN_FORMATTING_LEFT = CurrencyFormatting(
    thousand_delimiter=".",
    decimal_delimiter=",",
    symbol_space=False,
    symbol_position="left",
)
EUROPEAN_FORMATTING_LEFT_SPACED = CurrencyFormatting(
    thousand_delimiter=".",
    decimal_delimiter=",",
    symbol_space=True,
    symbol_position="left",
)
EUROPEAN_FORMATTING_RIGHT_SPACED = CurrencyFormatting(
    thousand_delimiter=".",
    decimal_delimiter=",",
    symbol_space=True,
    symbol_position="right",
)

SPACED_FORMAT = CurrencyFormatting(
    thousand_delimiter=" ",
    decimal_delimiter=",",
    symbol_space=True,
    symbol_position="right",
)

# Useful places to find currencies formats:
# https://www.freeformatter.com/i18n-standards-code-snippets.html
# https://lh.2xlibre.net/

DEFAULT_CURRENCY_FORMAT = AMERICAN_FORMATTING_LEFT

KNOWN_CURRENCY_FORMAT_MAP: Dict[str, CurrencyFormatting] = {
    "AED": AMERICAN_FORMATTING_LEFT_SPACED,
    "ARS": EUROPEAN_FORMATTING_LEFT_SPACED,
    "AUD": AMERICAN_FORMATTING_LEFT,
    "BDT": AMERICAN_FORMATTING_LEFT_SPACED,
    "BGN": SPACED_FORMAT,
    "BRL": EUROPEAN_FORMATTING_LEFT_SPACED,
    "CAD": AMERICAN_FORMATTING_LEFT,
    "CHF": EUROPEAN_FORMATTING_LEFT,
    "CNY": AMERICAN_FORMATTING_LEFT_SPACED,
    "COP": AMERICAN_FORMATTING_LEFT_SPACED,
    "DKK": EUROPEAN_FORMATTING_LEFT_SPACED,
    "EUR": EUROPEAN_FORMATTING_LEFT,
    "GBP": AMERICAN_FORMATTING_LEFT,
    "GHS": AMERICAN_FORMATTING_RIGHT_SPACED,
    "GTQ": AMERICAN_FORMATTING_LEFT_SPACED,
    "HKD": AMERICAN_FORMATTING_LEFT,
    "HRK": EUROPEAN_FORMATTING_LEFT_SPACED,
    "HUF": EUROPEAN_FORMATTING_RIGHT_SPACED,
    "IDR": EUROPEAN_FORMATTING_LEFT,
    "ILS": AMERICAN_FORMATTING_LEFT_SPACED,
    "INR": AMERICAN_FORMATTING_LEFT_SPACED,
    "JMD": AMERICAN_FORMATTING_LEFT,
    "JPY": AMERICAN_FORMATTING_LEFT,
    "KRW": AMERICAN_FORMATTING_LEFT,
    "MDL": EUROPEAN_FORMATTING_RIGHT_SPACED,
    "MXN": AMERICAN_FORMATTING_LEFT,
    "NGN": AMERICAN_FORMATTING_LEFT,
    "NOK": AMERICAN_FORMATTING_LEFT_SPACED,
    "NZD": AMERICAN_FORMATTING_LEFT,
    "PEN": AMERICAN_FORMATTING_LEFT,
    "PHP": AMERICAN_FORMATTING_LEFT,
    "PLN": SPACED_FORMAT,
    "RON": EUROPEAN_FORMATTING_RIGHT_SPACED,
    "RUB": SPACED_FORMAT,
    "SEK": EUROPEAN_FORMATTING_RIGHT_SPACED,
    "SGD": AMERICAN_FORMATTING_LEFT,
    "THB": AMERICAN_FORMATTING_LEFT_SPACED,
    "TRY": AMERICAN_FORMATTING_RIGHT_SPACED,
    "TWD": AMERICAN_FORMATTING_LEFT_SPACED,
    "UAH": EUROPEAN_FORMATTING_LEFT,
    "USD": AMERICAN_FORMATTING_LEFT,
    "UYU": EUROPEAN_FORMATTING_LEFT_SPACED,
    "ZAR": AMERICAN_FORMATTING_LEFT,
}
