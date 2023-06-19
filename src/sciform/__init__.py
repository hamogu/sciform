__version__ = "0.17.0"

# TODO: PDG sig figs
# TODO: get exponent based on larger of val/unc

from sciform.formatter import Formatter
from sciform.float_formatting import sfloat, vufloat
from sciform.format_options import (
    set_global_defaults, reset_global_defaults,
    global_add_c_prefix, global_add_small_si_prefixes,
    global_add_ppth_form, global_reset_si_prefixes,
    global_reset_iec_prefixes, global_reset_parts_per_forms,
    print_global_defaults, GlobalDefaultsContext)
from sciform.modes import (FillMode, SignMode, GroupingSeparator, RoundMode,
                           ExpMode)

__all__ = ['__version__', 'Formatter', 'sfloat', 'set_global_defaults',
           'reset_global_defaults', 'global_add_c_prefix',
           'global_add_small_si_prefixes', 'global_reset_si_prefixes',
           'global_add_ppth_form', 'global_reset_iec_prefixes',
           'global_reset_parts_per_forms', 'print_global_defaults',
           'GlobalDefaultsContext', 'FillMode', 'SignMode',
           'GroupingSeparator', 'RoundMode', 'ExpMode', 'vufloat']
