"""
Rendered format options used in sciform backend formatting algorithm.

:class:`UserOptions` are converted into :class:`RenderedOptions`
internally at format time.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from pprint import pformat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sciform import modes


@dataclass(frozen=True)
class RenderedOptions:
    """Rendered options: All options populated and using Enum instead of Literal."""

    exp_mode: modes.ExpMode
    exp_val: int | type(modes.AutoExpVal)
    round_mode: modes.RoundMode
    ndigits: int | type(modes.AutoDigits)
    upper_separator: modes.UpperSeparators
    decimal_separator: modes.DecimalSeparators
    lower_separator: modes.LowerSeparators
    sign_mode: modes.SignMode
    fill_mode: modes.FillMode
    top_dig_place: int
    exp_format: modes.ExpFormat
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript_exp: bool
    latex: bool
    nan_inf_exp: bool
    bracket_unc: bool
    pdg_sig_figs: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unc_pm_whitespace: bool

    def __str__(self: RenderedOptions) -> str:
        options_dict = asdict(self)
        for key, value in options_dict.items():
            if isinstance(value, Enum):
                options_dict[key] = value.value
        return pformat(options_dict, sort_dicts=False)
