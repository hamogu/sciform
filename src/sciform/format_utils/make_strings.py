"""String assembly utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sciform.format_utils.exponents import get_exp_str
from sciform.format_utils.numbers import (
    get_top_dec_place,
)
from sciform.options.option_types import (
    DecimalSeparatorEnums,
    ExpFormatEnum,
    ExpModeEnum,
    SeparatorEnum,
    SignModeEnum,
)

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal


def get_sign_str(num: Decimal, sign_mode: SignModeEnum) -> str:
    """Get the format sign string."""
    if num < 0:
        # Always return "-" for negative numbers.
        sign_str = "-"
    elif num > 0:
        # Return "+", " ", or "" for positive numbers.
        if sign_mode is SignModeEnum.ALWAYS:
            sign_str = "+"
        elif sign_mode is SignModeEnum.SPACE:
            sign_str = " "
        elif sign_mode is SignModeEnum.NEGATIVE:
            sign_str = ""
        else:
            msg = f"Invalid sign mode {sign_mode}."
            raise ValueError(msg)
    elif sign_mode is SignModeEnum.ALWAYS or sign_mode is SignModeEnum.SPACE:
        # For anything else (typically 0, possibly nan) return " " in "+" and " " modes
        sign_str = " "
    else:
        # Otherwise return the empty string.
        sign_str = ""

    return sign_str


def get_pad_str(
        left_pad_char: str,
        top_dec_place: int,
        top_padded_dec_place: int
) -> str:
    """Get the string padding from top_dec_place place to top_padded_dec_place place."""
    if top_padded_dec_place > top_dec_place:
        pad_len = top_padded_dec_place - max(top_dec_place, 0)
        pad_str = left_pad_char * pad_len
    else:
        pad_str = ""
    return pad_str


def format_num_by_top_bottom_dig(
    num: Decimal,
    target_top_dec_place: int,
    target_bottom_dec_place: int,
    sign_mode: SignModeEnum,
    left_pad_char: str,
) -> str:
    """Format a number according to specified top and bottom decimal places."""
    print_prec = max(0, -target_bottom_dec_place)
    abs_mantissa_str = f"{abs(num):.{print_prec}f}"

    sign_str = get_sign_str(num, sign_mode)

    num_top_dec_place = get_top_dec_place(num)
    pad_str = get_pad_str(left_pad_char, num_top_dec_place, target_top_dec_place)
    return f"{sign_str}{pad_str}{abs_mantissa_str}"


def construct_val_unc_str(  # noqa: PLR0913
    val_mantissa_str: str,
    unc_mantissa_str: str,
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    decimal_separator: DecimalSeparatorEnums,
    *,
    paren_uncertainty: bool,
    pm_whitespace: bool,
    paren_uncertainty_trim: bool,
) -> str:
    """Construct the value/uncertainty part of the formatted string."""
    if not paren_uncertainty:
        pm_symb = "±"
        if pm_whitespace:
            pm_symb = f" {pm_symb} "
        val_unc_str = f"{val_mantissa_str}{pm_symb}{unc_mantissa_str}"
    else:
        if (
            paren_uncertainty_trim
            and unc_mantissa.is_finite()
            and val_mantissa.is_finite()
            and 0 < unc_mantissa < abs(val_mantissa)
        ):
            """
            Don't strip the unc_mantissa_str if val_mantissa is non-finite.
            Don't strip the unc_mantissa_str if unc_mantissa == 0 (because then the
              empty string would remain).
            Don't left strip the unc_mantissa_str if unc_mantissa >= val_mantissa
            """
            for separator in SeparatorEnum:
                if separator != decimal_separator:
                    unc_mantissa_str = unc_mantissa_str.replace(separator, "")
            unc_mantissa_str = unc_mantissa_str.lstrip("0" + decimal_separator)
        val_unc_str = f"{val_mantissa_str}({unc_mantissa_str})"
    return val_unc_str


def construct_val_unc_exp_str(  # noqa: PLR0913
    *,
    val_unc_str: str,
    exp_val: int,
    exp_mode: ExpModeEnum,
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str | None],
    extra_iec_prefixes: dict[int, str | None],
    extra_parts_per_forms: dict[int, str | None],
    capitalize: bool,
    superscript: bool,
    paren_uncertainty: bool,
) -> str:
    """Combine the val_unc_str into the final val_unc_exp_str."""
    exp_str = get_exp_str(
        exp_val=exp_val,
        exp_mode=exp_mode,
        exp_format=exp_format,
        capitalize=capitalize,
        superscript=superscript,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
    )

    if exp_str == "":
        val_unc_exp_str = val_unc_str
    elif paren_uncertainty:
        # No parentheses for paren_uncertainty, e.g. 123(4)e+03
        val_unc_exp_str = f"{val_unc_str}{exp_str}"
    else:
        # Wrapping parentheses for ± uncertainty, e.g. (123 ± 4)e+03
        val_unc_exp_str = f"({val_unc_str}){exp_str}"

    return val_unc_exp_str
