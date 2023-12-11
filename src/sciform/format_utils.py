"""Various formatting utilities."""

from __future__ import annotations

import re
from decimal import Decimal
from math import floor, log2
from typing import Literal, Union, cast

from sciform.modes import (
    AutoDigits,
    AutoExpVal,
    ExpDriver,
    ExpFormat,
    ExpMode,
    RoundMode,
    Separator,
    SignMode,
)
from sciform.prefix import (
    iec_val_to_prefix_dict,
    pp_val_to_prefix_dict,
    si_val_to_prefix_dict,
)

Number = Union[Decimal, float, int, str]


def get_top_digit(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    _, digits, exp = num.as_tuple()
    return len(digits) + exp - 1


def get_top_digit_binary(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    return floor(log2(abs(num)))


def get_bottom_digit(num: Decimal) -> int:
    """Get the decimal plac of a decimal's least significant digit."""
    if not num.is_finite():
        return 0
    _, _, exp = num.as_tuple()
    return exp


def get_fixed_exp(
    input_exp: int | type(AutoExpVal),
) -> Literal[0]:
    """Get the exponent for fixed or percent format modes."""
    if input_exp is not AutoExpVal and input_exp != 0:
        msg = 'Cannot set non-zero exponent in fixed point or percent exponent mode.'
        raise ValueError(msg)
    return 0


def get_scientific_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
) -> int:
    """Get the exponent for scientific formatting mode."""
    return get_top_digit(num) if input_exp is AutoExpVal else input_exp


def get_engineering_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    shifted: bool = False,
) -> int:
    """Get the exponent for engineering formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit(num)
        exp_val = exp_val // 3 * 3 if not shifted else (exp_val + 1) // 3 * 3
    else:
        if input_exp % 3 != 0:
            msg = (
                f'Exponent must be an integer multiple of 3 in engineering modes, not '
                f'{input_exp}.'
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_binary_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    iec: bool = False,
) -> int:
    """Get the exponent for binary formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit_binary(num)
        if iec:
            exp_val = (exp_val // 10) * 10
    else:
        if iec and input_exp % 10 != 0:
            msg = (
                f'Exponent must be an integer multiple of 10 in binary IEC mode, not '
                f'{input_exp}.'
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_mantissa_exp_base(
    num: Decimal,
    exp_mode: ExpMode,
    input_exp: int | type(AutoExpVal),
) -> tuple[Decimal, int, int]:
    """Get mantissa, exponent, and base for formatting a decimal number."""
    base = 2 if exp_mode is ExpMode.BINARY or exp_mode is ExpMode.BINARY_IEC else 10

    if num == 0 or not num.is_finite():
        mantissa = Decimal(num)
        exp = 0 if input_exp is AutoExpVal else input_exp
    else:
        if exp_mode is ExpMode.FIXEDPOINT or exp_mode is ExpMode.PERCENT:
            exp = get_fixed_exp(input_exp)
        elif exp_mode is ExpMode.SCIENTIFIC:
            exp = get_scientific_exp(num, input_exp)
        elif exp_mode is ExpMode.ENGINEERING:
            exp = get_engineering_exp(num, input_exp)
        elif exp_mode is ExpMode.ENGINEERING_SHIFTED:
            exp = get_engineering_exp(num, input_exp, shifted=True)
        elif exp_mode is ExpMode.BINARY:
            exp = get_binary_exp(num, input_exp)
        elif exp_mode is ExpMode.BINARY_IEC:
            exp = get_binary_exp(num, input_exp, iec=True)
        else:
            msg = f'Unhandled exponent mode {exp_mode}.'
            raise ValueError(msg)
        mantissa = num * Decimal(base) ** Decimal(-exp)
    mantissa = mantissa.normalize()
    return mantissa, exp, base


def get_standard_exp_str(base: int, exp_val: int, *, capitalize: bool = False) -> str:
    """Get standard (eg. 'e+02') exponent string."""
    base_exp_symbol_dict = {10: 'e', 2: 'b'}
    exp_symbol = base_exp_symbol_dict[base]
    if capitalize:
        exp_symbol = exp_symbol.capitalize()
    return f'{exp_symbol}{exp_val:+03d}'


def get_superscript_exp_str(base: int, exp_val: int) -> str:
    """Get superscript (e.g. '×10⁺²') exponent string."""  # noqa: RUF002
    sup_trans = str.maketrans('+-0123456789', '⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    exp_val_str = f'{exp_val}'.translate(sup_trans)
    return f'×{base}{exp_val_str}'


def get_prefix_dict(
    exp_format: ExpFormat,
    base: Literal[10, 2],
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
) -> dict[int, str]:
    """Resolve dictionary of prefix translations."""
    if exp_format is ExpFormat.PREFIX:
        if base == 10:
            prefix_dict = si_val_to_prefix_dict.copy()
            prefix_dict.update(extra_si_prefixes)
        elif base == 2:
            prefix_dict = iec_val_to_prefix_dict.copy()
            prefix_dict.update(extra_iec_prefixes)
        else:
            msg = f'Unhandled base {base}'
            raise ValueError(msg)
    elif exp_format is ExpFormat.PARTS_PER:
        prefix_dict = pp_val_to_prefix_dict.copy()
        prefix_dict.update(extra_parts_per_forms)
    else:
        msg = f'Unhandled ExpFormat, {exp_format}.'
        raise ValueError(msg)

    return prefix_dict


def get_exp_str(  # noqa: PLR0913
    *,
    exp_val: int,
    exp_mode: ExpMode,
    exp_format: ExpFormat,
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
    capitalize: bool,
    latex: bool,
    latex_trim_whitespace: bool,
    superscript: bool,
) -> str:
    """Get formatting exponent string."""
    if exp_mode is ExpMode.FIXEDPOINT:
        return ''
    if exp_mode is ExpMode.PERCENT:
        return '%'

    base = 2 if exp_mode is ExpMode.BINARY or exp_mode is ExpMode.BINARY_IEC else 10
    base = cast(Literal[10, 2], base)

    if exp_format is ExpFormat.PREFIX or exp_format is ExpFormat.PARTS_PER:
        text_exp_dict = get_prefix_dict(
            exp_format,
            base,
            extra_si_prefixes,
            extra_iec_prefixes,
            extra_parts_per_forms,
        )
        if exp_val in text_exp_dict and text_exp_dict[exp_val] is not None:
            exp_str = f' {text_exp_dict[exp_val]}'
            exp_str = exp_str.rstrip(' ')
            if latex:
                if latex_trim_whitespace:
                    exp_str = exp_str.lstrip(' ')
                exp_str = rf'\text{{{exp_str}}}'
            return exp_str

    if latex:
        return rf'\times {base}^{{{exp_val:+}}}'
    if superscript:
        return get_superscript_exp_str(base, exp_val)

    return get_standard_exp_str(base, exp_val, capitalize=capitalize)


def parse_standard_exp_str(exp_str: str) -> tuple[int, int]:
    """Extract base and exponent value from standard exponent string."""
    match = re.match(
        r"""
         ^
         (?P<exp_symbol>[eEbB])
         (?P<exp_val>[+-]\d+)
         $
         """,
        exp_str,
        re.VERBOSE,
    )

    exp_symbol = match.group('exp_symbol')
    symbol_to_base_dict = {'e': 10, 'b': 2}
    base = symbol_to_base_dict[exp_symbol.lower()]

    exp_val_str = match.group('exp_val')
    exp_val = int(exp_val_str)

    return base, exp_val


def get_sign_str(num: Decimal, sign_mode: SignMode) -> str:
    """Get the format sign string."""
    if num < 0:
        sign_str = '-'
    elif sign_mode is SignMode.ALWAYS:
        sign_str = '+'
    elif sign_mode is SignMode.SPACE:
        sign_str = ' '
    elif sign_mode is SignMode.NEGATIVE:
        sign_str = ''
    else:
        msg = f'Invalid sign mode {sign_mode}.'
        raise ValueError(msg)
    return sign_str


def get_pdg_round_digit(num: Decimal) -> int:
    """
    Determine the PDG rounding digit place to which to round.

    Calculate the appropriate digit place to round to according to the
    particle data group 3-5-4 rounding rules.

    See
    https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf
    Section 5.2
    """
    top_digit = get_top_digit(num)

    # Bring num to be between 100 and 1000.
    num_top_three_digs = num * Decimal(10) ** (Decimal(2) - Decimal(top_digit))
    num_top_three_digs.quantize(1)
    new_top_digit = get_top_digit(num_top_three_digs)
    num_top_three_digs = num_top_three_digs * 10 ** (2 - new_top_digit)
    if 100 <= num_top_three_digs <= 354:
        round_digit = top_digit - 1
    elif 355 <= num_top_three_digs <= 949:
        round_digit = top_digit
    elif 950 <= num_top_three_digs <= 999:
        """
        Here we set the round digit equal to the top digit. But since
        the top three digits are >= 950 this means they will be rounded
        up to 1000. So with round digit set to the top digit this will
        correspond to displaying two digits of uncertainty: "10".
        e.g. 123.45632 +/- 0.987 would be rounded as 123.5 +/- 1.0.
        """
        round_digit = top_digit
    else:  # pragma: no cover
        raise ValueError

    return round_digit


def get_round_digit(
    num: Decimal,
    round_mode: RoundMode,
    ndigits: int | type(AutoDigits),
    *,
    pdg_sig_figs: bool = False,
) -> int:
    """Get the digit place to which to round."""
    if round_mode is RoundMode.SIG_FIG:
        if ndigits is AutoDigits:
            if pdg_sig_figs:
                round_digit = get_pdg_round_digit(num)
            else:
                round_digit = get_bottom_digit(num)
        else:
            round_digit = get_top_digit(num) - (ndigits - 1)
    elif round_mode is RoundMode.DEC_PLACE:
        round_digit = get_bottom_digit(num) if ndigits is AutoDigits else -ndigits
    else:
        msg = f'Unhandled round mode: {round_mode}.'
        raise ValueError(msg)
    return round_digit


def get_fill_str(fill_char: str, top_digit: int, top_padded_digit: int) -> str:
    """Get the string filling from top_digit place to top_padded_digit place."""
    if top_padded_digit > top_digit:
        pad_len = top_padded_digit - max(top_digit, 0)
        pad_str = fill_char * pad_len
    else:
        pad_str = ''
    return pad_str


def format_num_by_top_bottom_dig(
    num: Decimal,
    target_top_digit: int,
    target_bottom_digit: int,
    sign_mode: SignMode,
    fill_char: str,
) -> str:
    """Format a number according to specified top and bottom digit places."""
    print_prec = max(0, -target_bottom_digit)
    abs_mantissa_str = f'{abs(num):.{print_prec}f}'

    sign_str = get_sign_str(num, sign_mode)

    num_top_digit = get_top_digit(num)
    fill_str = get_fill_str(fill_char, num_top_digit, target_top_digit)
    return f'{sign_str}{fill_str}{abs_mantissa_str}'


def latex_translate(input_str: str) -> str:
    """Translate elements of a string for Latex compatibility."""
    result_str = input_str
    replacements = (
        ('(', r'\left('),
        (')', r'\right)'),
        ('%', r'\%'),
        ('_', r'\_'),
        ('nan', r'\text{nan}'),
        ('NAN', r'\text{NAN}'),
        ('inf', r'\text{inf}'),
        ('INF', r'\text{INF}'),
    )
    for old_chars, new_chars in replacements:
        result_str = result_str.replace(old_chars, new_chars)
    return result_str


def round_val_unc(
    val: Decimal,
    unc: Decimal,
    ndigits: int | type[AutoDigits],
    *,
    use_pdg_sig_figs: bool = False,
) -> tuple[Decimal, Decimal, int]:
    """Simultaneously round the value and uncertainty."""
    if unc.is_finite() and unc != 0:
        round_digit = get_round_digit(
            unc,
            RoundMode.SIG_FIG,
            ndigits,
            pdg_sig_figs=use_pdg_sig_figs,
        )
        unc_rounded = round(unc, -round_digit)
    else:
        round_digit = get_round_digit(
            val,
            RoundMode.SIG_FIG,
            ndigits,
            pdg_sig_figs=False,
        )
        unc_rounded = unc
    if val.is_finite():
        val_rounded = round(val, -round_digit)
    else:
        val_rounded = val
    return val_rounded, unc_rounded, round_digit


def get_val_unc_exp(
    val: Decimal,
    unc: Decimal,
    exp_mode: ExpMode,
    input_exp: int,
) -> tuple[int, ExpDriver]:
    """Get exponent for value/uncertainty formatting."""
    if val.is_finite() and unc.is_finite():
        if abs(val) >= unc:
            exp_driver_type = ExpDriver.VAL
        else:
            exp_driver_type = ExpDriver.UNC
    elif val.is_finite():
        exp_driver_type = ExpDriver.VAL
    else:
        exp_driver_type = ExpDriver.UNC

    if exp_driver_type is ExpDriver.VAL:
        exp_driver_val = val
    elif exp_driver_type is ExpDriver.UNC:
        exp_driver_val = unc
    else:  # pragma: no cover
        raise ValueError

    _, exp_val, _ = get_mantissa_exp_base(
        exp_driver_val,
        exp_mode=exp_mode,
        input_exp=input_exp,
    )

    return exp_val, exp_driver_type


def get_val_unc_top_digit(
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    input_top_digit: int | AutoDigits,
    *,
    val_unc_match_widths: bool,
) -> int | AutoDigits:
    """Get top digit place for value/uncertainty formatting."""
    if val_unc_match_widths:
        val_top_digit = get_top_digit(val_mantissa)
        unc_top_digit = get_top_digit(unc_mantissa)
        new_top_digit = max(
            input_top_digit,
            val_top_digit,
            unc_top_digit,
        )
    else:
        new_top_digit = input_top_digit
    return new_top_digit


def get_val_unc_mantissa_exp_strs(
    val_mantissa_exp_str: str,
    unc_mantissa_exp_str: str,
    exp_driver_type: ExpDriver,
) -> tuple[str, str, str]:
    """Break val/unc mantissa/exp strings into mantissa strings and an exp string."""
    # Optional parentheses needed to handle (nan)e+00 case
    mantissa_exp_pattern = re.compile(
        r'^\(?(?P<mantissa_str>.*?)\)?(?P<exp_str>[eEbB].*?)?$',
    )
    val_match = mantissa_exp_pattern.match(val_mantissa_exp_str)
    val_mantissa_str = val_match.group('mantissa_str')

    unc_match = mantissa_exp_pattern.match(unc_mantissa_exp_str)
    unc_mantissa_str = unc_match.group('mantissa_str')

    if exp_driver_type is ExpDriver.VAL:
        exp_str = val_match.group('exp_str')
    elif exp_driver_type is ExpDriver.UNC:
        exp_str = unc_match.group('exp_str')
    else:
        msg = f'Invalid exp_driver_type: {exp_driver_type}.'
        raise ValueError(msg)

    return val_mantissa_str, unc_mantissa_str, exp_str


def construct_val_unc_str(  # noqa: PLR0913
    val_mantissa_str: str,
    unc_mantissa_str: str,
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    decimal_separator: Separator,
    *,
    bracket_unc: bool,
    latex: bool,
    pm_whitespace: bool,
    bracket_unc_remove_seps: bool,
) -> str:
    """Construct the value/uncertainty part of the formatted string."""
    if not bracket_unc:
        pm_symb = r'\pm' if latex else '±'
        if pm_whitespace:
            pm_symb = f' {pm_symb} '
        val_unc_str = f'{val_mantissa_str}{pm_symb}{unc_mantissa_str}'
    else:
        if unc_mantissa.is_finite() and val_mantissa.is_finite():
            if unc_mantissa == 0:
                unc_mantissa_str = '0'
            elif unc_mantissa < abs(val_mantissa):
                unc_mantissa_str = unc_mantissa_str.lstrip('0.,_ ')
        if bracket_unc_remove_seps:
            for separator in Separator:
                if separator == decimal_separator:
                    continue
                unc_mantissa_str = unc_mantissa_str.replace(separator, '')
                # TODO: bracket_unc_remove_seps unit test in tests, not just doctest.
            if unc_mantissa < abs(val_mantissa):
                # TODO: I think this raises an error if bracket_unc=True but either
                #   unc_mantissa or val_mantissa is non-finite.
                # Only removed "embedded" decimal symbol for unc < val
                unc_mantissa_str = unc_mantissa_str.replace(
                    decimal_separator,
                    '',
                )
        val_unc_str = f'{val_mantissa_str}({unc_mantissa_str})'
    return val_unc_str


def construct_val_unc_exp_str(  # noqa: PLR0913
    *,
    val_unc_str: str,
    exp_val: int,
    exp_mode: ExpMode,
    exp_format: ExpFormat,
    extra_si_prefixes: dict[int, str | None],
    extra_iec_prefixes: dict[int, str | None],
    extra_parts_per_forms: dict[int, str | None],
    capitalize: bool,
    latex: bool,
    superscript_exp: bool,
    bracket_unc: bool,
) -> str:
    """Combine the val_unc_str into the final val_unc_exp_str."""
    exp_str = get_exp_str(
        exp_val=exp_val,
        exp_mode=exp_mode,
        exp_format=exp_format,
        capitalize=capitalize,
        latex=latex,
        latex_trim_whitespace=True,
        superscript=superscript_exp,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
    )

    """
    "1234(12)" val_unc_str along with exp_str "k" will be formatted as
    "1234(12) k whereas 1234(12) with exp_str "e+03" will be
    formatted as (1234(12))e+03.
    "1234 ± 12" will be formatted with parentheses as "(1234 ± 12) k" or
    "(1234 ± 12)e+03"
    """
    if bracket_unc and not re.match(r'^[eEbB][+-]\d+$', exp_str):
        val_unc_exp_str = f'{val_unc_str}{exp_str}'
    else:
        val_unc_exp_str = f'({val_unc_str}){exp_str}'

    return val_unc_exp_str
