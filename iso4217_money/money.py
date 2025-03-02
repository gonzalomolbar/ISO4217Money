from __future__ import annotations

from decimal import Decimal
from typing import Any, Callable

from iso4217_money.currency import Currency
from iso4217_money.types import AmountTypeAllowed, AmountTypeAllowedHint
from iso4217_money.utils import normalize_amount


def _binary_rich_comparison(operation: str) -> Callable[..., bool]:
    def _perform_binary_rich_comparison(
        self: Money,
        other: object,
        *args,
        **kwargs,
    ) -> bool:
        amount = self.amount
        currency = self.currency

        other_amount: Any
        if isinstance(other, Money):
            if currency != other.currency:
                raise TypeError(
                    "Unsupported Binary Rich Comparison Operation for Money of different currencies."
                )
            other_amount = other.amount
        elif isinstance(other, AmountTypeAllowed):
            other_amount = currency.round_to_decimals(other)
        else:
            other_amount = other

        operation_callable = getattr(amount, operation)

        return operation_callable(other_amount, *args, **kwargs)

    return _perform_binary_rich_comparison


def _unary_arithmetic_opp(
    operation: str,
) -> Callable[..., Money]:
    def _perform_unary_arithmetic_opp(
        self: Money,
        *args,
        **kwargs,
    ) -> Money:
        amount = self.amount
        currency = self.currency
        operation_callable = getattr(amount, operation)
        result = operation_callable(*args, **kwargs)
        return Money(currency=currency, amount=result)

    return _perform_unary_arithmetic_opp


def _binary_arithmetic_opp(
    operation: str,
) -> Callable[..., Money]:
    def _perform_binary_arithmetic_opp(
        self: Money,
        other: object,
        *args,
        **kwargs,
    ) -> Money:
        pass
        amount = self.amount
        currency = self.currency

        other_amount: Any
        if isinstance(other, Money):
            if currency != other.currency:
                raise TypeError(
                    "Unsupported Binary Arithmetic Operation for Money of different currencies."
                )
            other_amount = other.amount
        elif isinstance(other, AmountTypeAllowed):
            other_amount = currency.round_to_decimals(other)
        else:
            other_amount = other

        operation_callable = getattr(amount, operation)

        result = operation_callable(other_amount, *args, **kwargs)
        return Money(currency=currency, amount=result)

    return _perform_binary_arithmetic_opp


class Money:
    """Class containing a currency and its amount."""

    currency: Currency
    amount: Decimal

    __lt__ = _binary_rich_comparison(operation="__lt__")
    __le__ = _binary_rich_comparison(operation="__le__")
    __gt__ = _binary_rich_comparison(operation="__gt__")
    __ge__ = _binary_rich_comparison(operation="__ge__")

    __neg__ = _unary_arithmetic_opp("__neg__")
    __pos__ = _unary_arithmetic_opp("__pos__")
    __abs__ = _unary_arithmetic_opp("__abs__")
    __round__ = _unary_arithmetic_opp("__round__")
    __trunc__ = _unary_arithmetic_opp("__trunc__")
    __floor__ = _unary_arithmetic_opp("__floor__")
    __ceil__ = _unary_arithmetic_opp("__ceil__")

    __add__ = _binary_arithmetic_opp(operation="__add__")
    __radd__ = _binary_arithmetic_opp(operation="__radd__")
    __sub__ = _binary_arithmetic_opp(operation="__sub__")
    __rsub__ = _binary_arithmetic_opp(operation="__rsub__")
    __mul__ = _binary_arithmetic_opp(operation="__mul__")
    __rmul__ = _binary_arithmetic_opp(operation="__rmul__")
    __truediv__ = _binary_arithmetic_opp(operation="__truediv__")
    __rtruediv__ = _binary_arithmetic_opp(operation="__rtruediv__")
    __floordiv__ = _binary_arithmetic_opp(operation="__floordiv__")
    __rfloordiv__ = _binary_arithmetic_opp(operation="__rfloordiv__")
    __mod__ = _binary_arithmetic_opp(operation="__mod__")
    __rmod__ = _binary_arithmetic_opp(operation="__rmod__")
    __pow__ = _binary_arithmetic_opp(operation="__pow__")
    __rpow__ = _binary_arithmetic_opp(operation="__rpow__")

    def __init__(
        self,
        currency: Currency,
        amount: AmountTypeAllowedHint,
    ) -> None:
        normalized_amount = normalize_amount(amount)

        self.currency = currency
        self.amount = currency.round_to_decimals(normalized_amount)

    def to_string(self, with_code: bool = False) -> str:
        """Stringify the object.

        Args:
            with_code (bool): If we should append the currency code besides the symbol.

        Returns:
            str: String representing the amount in the correct currency format.
        """
        return self.currency.to_string(self.amount, with_code)

    def __str__(self) -> str:
        """Stringify the object.

        Returns:
            str: String representing the amount in the correct currency format.
        """
        return self.to_string()

    def __repr__(self) -> str:
        """Get a stringified representation of the object.

        NOTE:
            As any representation, runnin `eval()` in the result should return a object with the same values.

        Returns:
            str: Representation of the object..
        """
        return f"{repr(self.currency)}({self.amount})"

    def __hash__(self) -> int:
        """Implement the `hashing` operator for a Money.

        Based off the equality defined on `__eq__`

        Returns:
            int: Currency hash
        """
        return hash((self.amount, self.currency))

    def __eq__(self, other: object) -> bool:
        """Overload the `==` operator for a Currency.

        Args:
            other (object):
                Object that will be compared. Should be a `Currency` to evaluate

        Returns:
            bool: Either if the Currency object is considered equal to other
        """
        amount = self.amount
        currency = self.currency

        other_amount: Any
        if isinstance(other, Money):
            if currency != other.currency:
                return False
            other_amount = other.amount
        elif isinstance(other, AmountTypeAllowed):
            other_amount = currency.round_to_decimals(other)
        else:
            other_amount = other

        return amount == other_amount
