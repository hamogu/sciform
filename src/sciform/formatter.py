"""Main Formatter class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sciform.formatting import format_from_options
from sciform.options.conversion import populate_options
from sciform.options.input_options import InputOptions

if TYPE_CHECKING:  # pragma: no cover
    from sciform import modes
    from sciform.format_utils import Number
    from sciform.formatting import FormattedNumber
    from sciform.options.populated_options import PopulatedOptions


class Formatter:
    r"""
    Class to format value and value/uncertainty pairs.

    :class:`Formatter` is used to convert value and value/uncertainty
    pairs into formatted strings according to a variety of formatting
    options. See :ref:`formatting_options` for more details on the
    available options. Any options which are not populated (not passed
    in or passed in the ``None`` value) will be populated at format time
    by the corresponding values in the globally configured default
    options. See :ref:`global_config` for details about how to view and
    modify the global options. The user supplied options cannot be
    updated after the :class:`Formatter` is constructed.

    After initialization, the :class:`Formatter` is used by passing in
    a value into the :class:`Formatter`.

    >>> from sciform import Formatter
    >>> formatter = Formatter(exp_mode="engineering", round_mode="sig_fig", ndigits=4)
    >>> print(formatter(12345.678))
    12.35e+03

    A value/uncertainty pair can also be passed into the
    :class:`Formatter`.

    >>> formatter = Formatter(
    ...     exp_mode="engineering",
    ...     round_mode="sig_fig",
    ...     ndigits=2,
    ...     superscript=True,
    ... )
    >>> formatted = formatter(12345.678, 3.4)
    >>> print(formatted)
    (12.3457 ± 0.0034)×10³

    The returned object behaves like a ``str``, but is, in fact, a
    :class:`FormattedNumber` instance. The :class:`FormattedNumber` is
    a subclass of ``str`` but provides methods for post-conversion into
    LaTeX, HTML, and ASCII formats.

    >>> print(formatted.as_latex())
    $(12.3457\:\pm\:0.0034)\times10^{3}$
    >>> print(formatted.as_html())
    (12.3457 ± 0.0034)×10<sup>3</sup>
    >>> print(formatted.as_ascii())
    (12.3457 +/- 0.0034)e+03

    The formatting options input by the user can be checked by
    inspecting the :attr:`input_options` property

    >>> print(formatter.input_options)
    InputOptions(
     'exp_mode': 'engineering',
     'round_mode': 'sig_fig',
     'ndigits': 2,
     'superscript': True,
    )

    Only explicitly populated options appear in the string printout.
    However, populated and unpopulated parameters can be inspected by
    direct attribute access. Unpopulated parameters are ``None``-valued.

    >>> print(formatter.input_options.round_mode)
    sig_fig
    >>> print(formatter.input_options.exp_format)
    None

    The :meth:`InputOptions.as_dict` method returns a dictionary of
    input options that can be passed back into a :class:`Formatter`
    constructor as ``**kwargs``, possibly after modification. Only
    explicitly populated options are included in this dictionary.

    >>> print(formatter.input_options.as_dict())
    {'exp_mode': 'engineering', 'round_mode': 'sig_fig', 'ndigits': 2, 'superscript': True}

    Likewise, the result of populating the options with the global
    options can be previewed by inspecting the :attr:`populated_options`
    property.

    >>> print(formatter.populated_options)
    PopulatedOptions(
     'exp_mode': 'engineering',
     'exp_val': AutoExpVal,
     'round_mode': 'sig_fig',
     'ndigits': 2,
     'upper_separator': '',
     'decimal_separator': '.',
     'lower_separator': '',
     'sign_mode': '-',
     'left_pad_char': ' ',
     'left_pad_dec_place': 0,
     'exp_format': 'standard',
     'extra_si_prefixes': {},
     'extra_iec_prefixes': {},
     'extra_parts_per_forms': {},
     'capitalize': False,
     'superscript': True,
     'nan_inf_exp': False,
     'paren_uncertainty': False,
     'pdg_sig_figs': False,
     'left_pad_matching': False,
     'paren_uncertainty_separators': True,
     'pm_whitespace': True,
    )
    >>> print(formatter.populated_options.exp_format)
    standard

    The :class:`PopulatedOptions` class also provides a
    :class:`PopulatedOptions.as_dict` method which can be used to
    construct ``**kwargs`` to pass into new :class:`Formatter`
    instances.

    """

    def __init__(  # noqa: PLR0913
        self: Formatter,
        *,
        exp_mode: modes.ExpMode | None = None,
        exp_val: int | type(modes.AutoExpVal) | None = None,
        round_mode: modes.RoundMode | None = None,
        ndigits: int | type(modes.AutoDigits) | None = None,
        upper_separator: modes.UpperSeparators | None = None,
        decimal_separator: modes.DecimalSeparators | None = None,
        lower_separator: modes.LowerSeparators | None = None,
        sign_mode: modes.SignMode | None = None,
        left_pad_char: modes.LeftPadChar | Literal[0] | None = None,
        left_pad_dec_place: int | None = None,
        exp_format: modes.ExpFormat | None = None,
        extra_si_prefixes: dict[int, str] | None = None,
        extra_iec_prefixes: dict[int, str] | None = None,
        extra_parts_per_forms: dict[int, str] | None = None,
        capitalize: bool | None = None,
        superscript: bool | None = None,
        nan_inf_exp: bool | None = None,
        paren_uncertainty: bool | None = None,
        pdg_sig_figs: bool | None = None,
        left_pad_matching: bool | None = None,
        paren_uncertainty_separators: bool | None = None,
        pm_whitespace: bool | None = None,
        add_c_prefix: bool | None = None,
        add_small_si_prefixes: bool | None = None,
        add_ppth_form: bool | None = None,
    ) -> None:
        """
        Create a new ``Formatter``.

        The following checks are performed when creating a new
        :class:`Formatter` object:

        * ``ndigits`` >= 1 for significant figure rounding mode
        * ``exp_val`` must be consistent with the exponent mode. If
          ``exp_val`` is specified (i.e. not ``None``) and ``exp_val``
          is not ``AutoExpVal`` then

          * ``exp_val`` must be 0 for fixed point and percent modes
          * ``exp_val`` must be a multiple of 3 for engineering and
            shifted engineering modes
          * ``exp_val`` must be a multiple of 10 for binary iec mode

        * ``upper_separator`` may be any of ``['', ',', '.', ' ', '_']``
          but must be different from ``decimal_separator``
        * ``decimal_separator`` may be any of ``['.', ',']``
        * ``lower_separator`` may be any of ``['', ' ', '_']``

        :param exp_mode: Specify the formatting mode.
        :type exp_mode: ``Literal['fixed_point', 'percent',
          'scientific', 'engineering', 'engineering_shifted', 'binary',
          'binary_iec'] | None``
        :param exp_val: Indicates how the exponent value should be
          chosen. If an integer is specified, the value must be 0 for
          fixed point and percent modes, an integer multiple of 3 for
          engineering and engineering shifted modes, and an integer
          multiple of 10 for binary IEC mode.
        :type exp_val: ``int | type[AutoExpVal] | None``
        :param round_mode: Indicate how to round numbers during
          formatting.
        :type round_mode: ``Literal['sig_fig', 'dec_place'] | None``
        :param ndigits: Indicate how the many significant digits or the
          decimal place to use for rounding. Must be >= 1 for
          significant figure rounding. Can be any integer for decimal
          place rounding.
        :type ndigits: ``int | type[AutoDigits] | None``
        :param upper_separator: Separator character to be used to group
          digits above the decimal symbol.
        :type upper_separator: ``Literal['', ',', '.', ' ', '_'] | None``
        :param decimal_separator: Separator character to be used as the
          decimal symbol. Note that ``decimal_separator`` cannot be the
          same as ``upper_separator``
        :type decimal_separator: ``Literal['.', ','] | None``
        :param lower_separator: Separator character to be used to group
          digits below the decimal symbol.
        :type lower_separator: ``Literal['', ' ', '_'] | None``
        :param sign_mode: Indicate sign symbol behavior.
        :type sign_mode: ``Literal['-', '+', ' '] | None``
        :param left_pad_char: Indicate whether to pad with zeros or
          spaces.
        :type left_pad_char: ``Literal[' ', '0', 0] | None``
        :param left_pad_dec_place: Positive ``int`` indicating the
          decimal place to which the string will be left padded before
          the sign symbol. 0 corresponds to the ones place, 1
          corresponds to the tens place etc. E.g.
          ``left_pad_dec_place=4`` will convert ``12`` into
          ``00012``.
        :type left_pad_dec_place: ``int | None``
        :param exp_format: Indicate how exponents should be presented.
        :type exp_format: ``Literal['standard', 'prefix', 'parts_per'] | None``
        :param extra_si_prefixes: Dictionary mapping additional exponent
          values to si prefixes. Entries overwrite default values. A
          value of ``None`` means that exponent will not be converted.
        :type extra_si_prefixes: ``dict[int, Union[str, None]] | None``
        :param extra_iec_prefixes: Dictionary mapping additional
          exponent values to iec prefixes. Entries overwrite default
          values. A value of ``None`` means that exponent will not be
          converted.
        :type extra_iec_prefixes: ``dict[int, Union[str, None]] | None``
        :param extra_parts_per_forms: Dictionary mapping additional
          exponent values to "parts-per" forms. Entries overwrite
          default values. A value of ``None`` means that exponent will
          not be converted.
        :type extra_parts_per_forms: ``dict[int, Union[str, None]] | None``
        :param capitalize: Flag indicating whether the exponentiation
          symbol should be upper- or lower-case.
        :type capitalize: ``bool | None``
        :param superscript: Flag indicating if the exponent string
          should be converted into superscript notation. E.g.
          ``'1.23e+02'`` is converted to ``'1.23×10²'``
        :type superscript: ``bool | None``
        :param nan_inf_exp: Flag indicating whether non-finite numbers
          such as ``float('nan')`` or ``float('inf')`` should be
          formatted with exponent symbols when exponent modes including
          exponent symbols are selected.
        :type nan_inf_exp: ``bool | None``
        :param paren_uncertainty: Flag indicating if parentheses
          uncertainty mode (e.g. ``12.34(82)`` instead of
          ``12.34 ± 0.82``) should be used.
        :type paren_uncertainty: ``bool | None``
        :param pdg_sig_figs: Flag indicating whether the
          particle-data-group conventions should be used to
          automatically determine the number of significant figures to
          use for uncertainty. Ignored for single value formatting.
        :type pdg_sig_figs: ``bool | None``
        :param left_pad_matching: Flag indicating if the value or
          uncertainty should be left padded to ensure they are both left
          padded to the same digits place.
        :type left_pad_matching: ``bool | None``
        :param paren_uncertainty_separators: Flag indicating if
          separator symbols should be included in the uncertainty when
          using parentheses uncertainty mode. E.g. expressing
          ``123.4 ± 2.3`` either as ``123.4(2.3)`` or ``123.4(23)``.
        :type paren_uncertainty_separators: ``bool | None``
        :param pm_whitespace: Flag indicating if there should be
          whitespace surrounding the ``'±'`` symbols when formatting.
          E.g. ``123.4±2.3`` compared to ``123.4 ± 2.3``.
        :type pm_whitespace: ``bool | None``
        :param add_c_prefix: (default ``False``) If ``True``, adds
          ``{-2: 'c'}`` to ``extra_si_prefixes``.
        :type add_c_prefix: ``bool``
        :param add_small_si_prefixes: (default ``False``) If ``True``, adds
          ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
          ``extra_si_prefixes``.
        :type add_small_si_prefixes: ``bool``
        :param add_ppth_form: (default ``False``) if ``True``, adds
          ``{-3: 'ppth'}`` to ``extra_parts_per_forms``.
        :type add_ppth_form: ``bool``
        """
        self._input_options = InputOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            left_pad_char=left_pad_char,
            left_pad_dec_place=left_pad_dec_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript=superscript,
            nan_inf_exp=nan_inf_exp,
            paren_uncertainty=paren_uncertainty,
            pdg_sig_figs=pdg_sig_figs,
            left_pad_matching=left_pad_matching,
            paren_uncertainty_separators=paren_uncertainty_separators,
            pm_whitespace=pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form,
        )

    @property
    def input_options(self: Formatter) -> InputOptions:
        """Return user input options as :class:`InputOptions` instance."""
        return self._input_options

    @property
    def populated_options(self: Formatter) -> PopulatedOptions:
        """
        Return fully populated options as :class:`PopulatedOptions` instance.

        At format time any input options which were not specified (or
        which were passed in ``None`` values) are populated with the
        corresponding values from the global options. The result of
        this merging can be accessed via the ``populated_options``
        property which provides a :class:`PopulatedOptions` instance.
        The ``populated_options`` property is recalculated using the
        input options and the global options at access time, so the
        result is reflective of the current state of the global options.

        Note that the ``add_c_prefix``, ``add_small_si_prefixes`` and
        ``add_ppth_form`` options do not appear in the populated
        options. Instead, if any of these are ``True``, they result in
        modification of the ``extra_si_prefixes`` or
        ``extra_parts_per_forms`` attributes in the populated options.
        Also note that e.g. if ``extra_si_prefixes`` is not passed in,
        or remains ``None``, but ``add_c_prefix`` is ``True``, then the
        options will behave as if ``extra_si_prefixes = {-2: "c"}``.
        That is, importantly, ``extra_si_prefixes`` will **not** be
        populated by the global options even though its value was not
        explicit set during options configuration.
        """
        return populate_options(self.input_options)

    def __call__(
        self: Formatter,
        value: Number,
        uncertainty: Number | None = None,
        /,
    ) -> FormattedNumber:
        """
        Format a value or value/uncertainty pair.

        :param value: Value to be formatted.
        :type value: ``Decimal | float | int | str``
        :param uncertainty: Optional uncertainty to be formatted.
        :type uncertainty: ``Decimal | float | int | str | None``
        """
        return format_from_options(
            value,
            uncertainty,
            input_options=self.input_options,
        )
