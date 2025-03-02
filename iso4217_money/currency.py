"""Main entry point for Teampay's Currencies implementation."""

from __future__ import annotations

import logging
import re
from contextlib import suppress
from decimal import ROUND_HALF_UP, Decimal
from typing import TYPE_CHECKING


from iso4217_money.currency_formatting import (
    DEFAULT_CURRENCY_FORMAT,
    KNOWN_CURRENCY_FORMAT_MAP,
    CurrencyFormatting,
)
from iso4217_money.statics import (
    ALPHABETIC_CODE_TO_CURRENCY_SYMBOLS_MAP,
    ISO_4217_CURRENCIES,
    NUMERIC_CODE_TO_ISO_4217_CURRENCY_MAP,
    ALPHABETIC_CODE_TO_ISO_4217_CURRENCY_MAP,
)
from iso4217_money.types import AmountTypeAllowedHint
from iso4217_money.utils import normalize_amount

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from iso4217_money.money import Money


class Currency:
    """Class containing information and operations specific to a concrete Currency.

    To instantiate it it could be instantiated regularly (not the usual)
    or by calling the metaclass dunder methods that allows things like:

    'Currency[currency_code]`
    """

    def __init__(self, currency_code: str) -> None:
        iso_4217_currency = None
        with suppress(KeyError):
            if re.match(r"^[a-zA-Z]{3}$", currency_code):
                # We received the 3 letter code of the ISO427
                iso_4217_currency = ALPHABETIC_CODE_TO_ISO_4217_CURRENCY_MAP[
                    currency_code
                ]
            elif re.match(r"^\d{3}$", currency_code):
                # We received the 3 digit code of the ISO427
                iso_4217_currency = NUMERIC_CODE_TO_ISO_4217_CURRENCY_MAP[currency_code]

        if iso_4217_currency is None:
            # It-should-not-happen scenario, we raise an exception for visualization
            LOGGER.exception(
                "Received a non-valid currency code when retrieving a currency.",
                extra={"currency_code": currency_code},
            )
            raise ValueError(
                f"Received a non-valid currency code when retrieving a currency: {currency_code}."
            )

        minimum_monetary_units_str = iso_4217_currency["minor_unit"]
        if minimum_monetary_units_str == "N.A.":
            LOGGER.exception(
                "Currency detected without `minimum_monetary_units`.",
                extra={"currency_code": currency_code},
            )
            raise ValueError(
                f"Currency detected without `minimum_monetary_units`: {minimum_monetary_units_str}."
            )
        try:
            minimum_monetary_units = int(minimum_monetary_units_str)
        except ValueError:
            LOGGER.error(
                "Currency detected with invalid `minimum_monetary_units`.",
                extra={"currency_code": currency_code},
            )
            raise ValueError(
                f"Currency detected with invalid `minimum_monetary_units`: {minimum_monetary_units_str}."
            )

        try:
            symbol = ALPHABETIC_CODE_TO_CURRENCY_SYMBOLS_MAP[
                iso_4217_currency["alphabetic_code"]
            ]
        except KeyError:
            # If it not in the list defined, either probably does not have a symbol or is new and it has to be updated
            symbol = ""

        formatting = KNOWN_CURRENCY_FORMAT_MAP.get(
            iso_4217_currency["alphabetic_code"],
            DEFAULT_CURRENCY_FORMAT,
        )

        self.name: str = iso_4217_currency["entity"]
        self.alphabetic_code: str = iso_4217_currency["alphabetic_code"]
        self.numeric_code: str = iso_4217_currency["numeric_code"]
        self.minimum_monetary_units: int = minimum_monetary_units
        self.symbol: str = symbol
        self.formatting: CurrencyFormatting = formatting

    @classmethod
    def all_currencies(cls) -> list[Currency]:
        """Get a list with all the currencies that we considered valid, coming from the ISO4217.

        Returns:
            list[Currency]: List with the Currency objects.
        """
        currencies = []
        for iso_currency in ISO_4217_CURRENCIES:
            alphabetic_code = iso_currency["alphabetic_code"]

            if alphabetic_code[0] == "X":
                # Per the ISO3166, all currency codes that start with "X" is set to define a "supranational",
                # meaning that is as such not a regular currency used by any country
                continue

            currencies.append(cls(alphabetic_code))
        return currencies

    def to_string(
        self, amount_raw: AmountTypeAllowedHint, with_code: bool = False
    ) -> str:
        """Stringify an amount for the specific format of the currency.

        Args:
            amount_raw (AmountTypeAllowedHint): Amount for the currency.
                We're open to receive a Decimal, float or int since we'll cast it into a Decimal either way.
            with_code (bool): If we should append the currency code besides the symbol.

        Returns:
            str: String representing the amount in the correct currency format.
        """
        amount = normalize_amount(amount_raw)

        # Round number
        amount = self.round_to_decimals(amount)

        # Set the number of decimals
        amount_str = f"{abs(amount):,.{self.minimum_monetary_units}f}"

        # Correct decimals and thousand delimiters if necessary
        amount_str = (
            amount_str.replace(",", "X")
            .replace(".", self.formatting.decimal_delimiter)
            .replace("X", self.formatting.thousand_delimiter)
        )

        # Add spaces around the symbol if necessary
        symbol = self.symbol
        if self.formatting.symbol_space:
            symbol = f" {symbol} "

        # Set the symbol where it belongs
        if self.formatting.symbol_position == "left":
            amount_str = f"{symbol}{amount_str}"
        elif self.formatting.symbol_position == "right":
            amount_str = f"{amount_str}{symbol}"

        # Strip extra spaces
        amount_str = amount_str.strip()

        # Set the negative symbol now after the format is finished
        if amount < 0:
            amount_str = f"-{amount_str}"

        # Add the currency code after the whole formatted amount if desired
        if with_code:
            amount_str += f" {self.alphabetic_code}"

        return amount_str

    def minimum_monetary_units_pow(self) -> Decimal:
        """Return the currency's minimum monetary units' power of ten."""
        return 10**self.minimum_monetary_units

    def round_to_decimals(self, amount_raw: AmountTypeAllowedHint) -> Decimal:
        """Round the amount sent to its closest decimal."""
        amount = normalize_amount(amount_raw)
        return amount.quantize(
            Decimal(1) / Decimal(self.minimum_monetary_units_pow()), ROUND_HALF_UP
        )

    def to_cents(self, amount: Decimal) -> int:
        """Convert a decimal amount to its minimum monetary unit amount equivalent."""
        amount_rounded = self.round_to_decimals(amount)
        return int(amount_rounded * self.minimum_monetary_units_pow())

    def from_cents(self, cents_amount: int) -> Decimal:
        """Convert a minimum monetary unit amount to its decimal amount equivalent."""
        return Decimal(cents_amount) / Decimal(self.minimum_monetary_units_pow())

    # region Dunder methods

    def __call__(self, amount_raw: AmountTypeAllowedHint) -> Money:
        """Return from the Currency object and the amount received the Money object for that pair.

        Args:
            amount_raw (AmountTypeAllowedHint): Amount that will be part of the Money object

        Returns:
            Money: Currency aware amount object.
        """
        from iso4217_money.money import Money

        return Money(currency=self, amount=amount_raw)

    def __str__(self) -> str:
        """Stringify the object.

        Returns:
            str: String with the currency code and name.
        """
        return f"{self.alphabetic_code} - {self.name}"

    def __repr__(self) -> str:
        """Get a stringified representation of the object.

        NOTE:
            As any representation, runnin `eval()` in the result should return a object with the same values.

        Returns:
            str: Representation of the object..
        """
        return f'Currency("{self.alphabetic_code}")'

    def __hash__(self) -> int:
        """Implement the `hashing` operator for a Currency.

        Based off the equality defined on `__eq__`

        Returns:
            int: Currency hash
        """
        return hash((self.alphabetic_code, self.numeric_code))

    def __eq__(self, other: object) -> bool:
        """Overload the `==` operator for a Currency.

        Args:
            other (object):
                Object that will be compared. Should be a `Currency` to evaluate

        Returns:
            bool: Either if the Currency object is considered equal to other
        """
        if isinstance(other, Currency):
            return (
                self.alphabetic_code == other.alphabetic_code
                and self.numeric_code == other.numeric_code
            )

        return False

    # endregion
