import unittest

from sciform import sfloat, GlobalDefaultsContext


FloatFSMLCases = list[tuple[float, list[tuple[str, str]]]]


class TestFormatting(unittest.TestCase):
    def run_float_fsml_cases(self, cases_list: FloatFSMLCases):
        for num, formats_list in cases_list:
            for format_spec, expected_num_str in formats_list:
                snum = sfloat(num)
                snum_str = f'{snum:{format_spec}}'
                with self.subTest(num=num, format_spec=format_spec,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_fixed_point(self):
        cases_list = [
            (123.456, [
                ('f', '123.456'),
                ('.-3f', '0'),
                ('.-2f', '100'),
                ('.-1f', '120'),
                ('.0f', '123'),
                ('.1f', '123.5'),
                ('.2f', '123.46'),
                ('.3f', '123.456'),
                ('.4f', '123.4560'),
                ('!1f', '100'),
                ('!2f', '120'),
                ('!3f', '123'),
                ('!4f', '123.5'),
                ('!5f', '123.46'),
                ('!6f', '123.456'),
                ('!7f', '123.4560')
            ]),
            (0.00062607, [
                ('f', '0.00062607'),
                ('.-1f', '0'),
                ('.0f', '0'),
                ('.1f', '0.0'),
                ('.2f', '0.00'),
                ('.3f', '0.001'),
                ('.4f', '0.0006'),
                ('.5f', '0.00063'),
                ('.6f', '0.000626'),
                ('.7f', '0.0006261'),
                ('.8f', '0.00062607'),
                ('.9f', '0.000626070'),
                ('!1f', '0.0006'),
                ('!2f', '0.00063'),
                ('!3f', '0.000626'),
                ('!4f', '0.0006261'),
                ('!5f', '0.00062607'),
                ('!6f', '0.000626070')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_percent(self):
        cases_list = [
            (0.123456, [
                ('%', '12.3456%'),
                ('.-3%', '0%'),
                ('.-2%', '0%'),
                ('.-1%', '10%'),
                ('.0%', '12%'),
                ('.1%', '12.3%'),
                ('.2%', '12.35%'),
                ('.3%', '12.346%'),
                ('.4%', '12.3456%'),
                ('!1%', '10%'),
                ('!2%', '12%'),
                ('!3%', '12.3%'),
                ('!4%', '12.35%'),
                ('!5%', '12.346%'),
                ('!6%', '12.3456%'),
                ('!7%', '12.34560%')
            ]),
            (0.00062607, [
                ('%', '0.062607%'),
                ('.-1%', '0%'),
                ('.0%', '0%'),
                ('.1%', '0.1%'),
                ('.2%', '0.06%'),
                ('.3%', '0.063%'),
                ('.4%', '0.0626%'),
                ('.5%', '0.06261%'),
                ('.6%', '0.062607%'),
                ('.7%', '0.0626070%'),
                ('.8%', '0.06260700%'),
                ('.9%', '0.062607000%'),
                ('!1%', '0.06%'),
                ('!2%', '0.063%'),
                ('!3%', '0.0626%'),
                ('!4%', '0.06261%'),
                ('!5%', '0.062607%'),
                ('!6%', '0.0626070%')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_scientific(self):
        cases_list = [
            (123.456, [
                ('e', '1.23456e+02'),
                ('.-3e', '0e+00'),
                ('.-2e', '0e+00'),
                ('.-1e', '0e+00'),
                ('.0e', '1e+02'),
                ('.1e', '1.2e+02'),
                ('.2e', '1.23e+02'),
                ('.3e', '1.235e+02'),
                ('.4e', '1.2346e+02'),
                ('!1e', '1e+02'),
                ('!2e', '1.2e+02'),
                ('!3e', '1.23e+02'),
                ('!4e', '1.235e+02'),
                ('!5e', '1.2346e+02'),
                ('!6e', '1.23456e+02'),
                ('!7e', '1.234560e+02')
            ]),
            (0.00062607, [
                ('e', '6.2607e-04'),
                ('.-2e', '0e+00'),
                ('.-1e', '0e+00'),
                ('.0e', '6e-04'),
                ('.1e', '6.3e-04'),
                ('.2e', '6.26e-04'),
                ('.3e', '6.261e-04'),
                ('.4e', '6.2607e-04'),
                ('.5e', '6.26070e-04'),
                ('.6e', '6.260700e-04'),
                ('!1e', '6e-04'),
                ('!2e', '6.3e-04'),
                ('!3e', '6.26e-04'),
                ('!4e', '6.261e-04'),
                ('!5e', '6.2607e-04'),
                ('!6e', '6.26070e-04'),
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_engineering(self):
        cases_list = [
            (123.456, [
                ('r', '123.456e+00'),
                ('.-3r', '0e+00'),
                ('.-2r', '100e+00'),
                ('.-1r', '120e+00'),
                ('.0r', '123e+00'),
                ('.1r', '123.5e+00'),
                ('.2r', '123.46e+00'),
                ('.3r', '123.456e+00'),
                ('.4r', '123.4560e+00'),
                ('!1r', '100e+00'),
                ('!2r', '120e+00'),
                ('!3r', '123e+00'),
                ('!4r', '123.5e+00'),
                ('!5r', '123.46e+00'),
                ('!6r', '123.456e+00'),
                ('!7r', '123.4560e+00')
            ]),
            (1234.56, [
                ('r', '1.23456e+03'),
                ('.-3r', '0e+00'),
                ('.-2r', '0e+00'),
                ('.-1r', '0e+00'),
                ('.0r', '1e+03'),
                ('.1r', '1.2e+03'),
                ('.2r', '1.23e+03'),
                ('.3r', '1.235e+03'),
                ('.4r', '1.2346e+03'),
                ('.5r', '1.23456e+03'),
                ('!1r', '1e+03'),
                ('!2r', '1.2e+03'),
                ('!3r', '1.23e+03'),
                ('!4r', '1.235e+03'),
                ('!5r', '1.2346e+03'),
                ('!6r', '1.23456e+03'),
                ('!7r', '1.234560e+03')
            ]),
            (12345.6, [
                ('r', '12.3456e+03'),
                ('.-3r', '0e+00'),
                ('.-2r', '0e+00'),
                ('.-1r', '10e+03'),
                ('.0r', '12e+03'),
                ('.1r', '12.3e+03'),
                ('.2r', '12.35e+03'),
                ('.3r', '12.346e+03'),
                ('.4r', '12.3456e+03'),
                ('.5r', '12.34560e+03'),
                ('!1r', '10e+03'),
                ('!2r', '12e+03'),
                ('!3r', '12.3e+03'),
                ('!4r', '12.35e+03'),
                ('!5r', '12.346e+03'),
                ('!6r', '12.3456e+03'),
                ('!7r', '12.34560e+03')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_engineering_shifted(self):
        cases_list = [
            (123.456, [
                ('#r', '0.123456e+03'),
                ('#.-3r', '0e+00'),
                ('#.-2r', '0e+00'),
                ('#.-1r', '0e+00'),
                ('#.0r', '0e+00'),
                ('#.1r', '0.1e+03'),
                ('#.2r', '0.12e+03'),
                ('#.3r', '0.123e+03'),
                ('#.4r', '0.1235e+03'),
                ('#!1r', '0.1e+03'),
                ('#!2r', '0.12e+03'),
                ('#!3r', '0.123e+03'),
                ('#!4r', '0.1235e+03'),
                ('#!5r', '0.12346e+03'),
                ('#!6r', '0.123456e+03'),
                ('#!7r', '0.1234560e+03')
            ]),
            (1234.56, [
                ('#r', '1.23456e+03'),
                ('#.-3r', '0e+00'),
                ('#.-2r', '0e+00'),
                ('#.-1r', '0e+00'),
                ('#.0r', '1e+03'),
                ('#.1r', '1.2e+03'),
                ('#.2r', '1.23e+03'),
                ('#.3r', '1.235e+03'),
                ('#.4r', '1.2346e+03'),
                ('#.5r', '1.23456e+03'),
                ('#!1r', '1e+03'),
                ('#!2r', '1.2e+03'),
                ('#!3r', '1.23e+03'),
                ('#!4r', '1.235e+03'),
                ('#!5r', '1.2346e+03'),
                ('#!6r', '1.23456e+03'),
                ('#!7r', '1.234560e+03')
            ]),
            (12345.6, [
                ('#r', '12.3456e+03'),
                ('#.-3r', '0e+00'),
                ('#.-2r', '0e+00'),
                ('#.-1r', '10e+03'),
                ('#.0r', '12e+03'),
                ('#.1r', '12.3e+03'),
                ('#.2r', '12.35e+03'),
                ('#.3r', '12.346e+03'),
                ('#.4r', '12.3456e+03'),
                ('#.5r', '12.34560e+03'),
                ('#!1r', '10e+03'),
                ('#!2r', '12e+03'),
                ('#!3r', '12.3e+03'),
                ('#!4r', '12.35e+03'),
                ('#!5r', '12.346e+03'),
                ('#!6r', '12.3456e+03'),
                ('#!7r', '12.34560e+03')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_exp(self):
        cases_list = [
            (123.456, [
                ('ex-4', '1234560e-04'),
                ('ex-3', '123456e-03'),
                ('ex-2', '12345.6e-02'),
                ('ex-1', '1234.56e-01'),
                ('ex+0', '123.456e+00'),
                ('ex+1', '12.3456e+01'),
                ('ex+2', '1.23456e+02'),
                ('ex+3', '0.123456e+03'),
                ('ex+4', '0.0123456e+04'),
                ('ex1', '12.3456e+01'),
                ('ex2', '1.23456e+02'),
                ('ex3', '0.123456e+03'),
                ('ex4', '0.0123456e+04'),
                ('rx0', '123.456e+00'),
                ('rx-3', '123456e-03'),
                ('rx+3', '0.123456e+03')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_rounding(self):
        cases_list = [
            (99.99, [
                ('', '99.99'),
                ('e', '9.999e+01'),
                ('.1e', '1.0e+02'),
                ('.2e', '1.00e+02'),
                ('.3e', '9.999e+01'),
                ('!1e', '1e+02'),
                ('!2e', '1.0e+02'),
                ('!3e', '1.00e+02'),
                ('!4e', '9.999e+01')
            ]),
            (999.99, [
                ('.0r', '1e+03'),
                ('.1r', '1.0e+03'),
                ('.2r', '999.99e+00'),
                ('.3r', '999.990e+00'),
                ('.4r', '999.9900e+00'),
                ('!1r', '1e+03'),
                ('!2r', '1.0e+03'),
                ('!3r', '1.00e+03'),
                ('!4r', '1.000e+03'),
                ('!5r', '999.99e+00'),
                ('!6r', '999.990e+00')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_zero(self):
        cases_list = [
            (0, [
                ('', '0'),
                ('f', '0'),
                ('e', '0e+00'),
                ('r', '0e+00'),
                ('#r', '0e+00'),
                ('.3', '0.000'),
                ('.3f', '0.000'),
                ('.3e', '0.000e+00'),
                ('.3r', '0.000e+00'),
                ('#.3r', '0.000e+00'),
                ('!3', '0.00'),
                ('!3f', '0.00'),
                ('!3e', '0.00e+00'),
                ('!3r', '0.00e+00'),
                ('#!3r', '0.00e+00'),
                ('0=2.3', '000.000'),
                ('0=2.3f', '000.000'),
                ('0=2.3e', '000.000e+00'),
                ('0=2.3r', '000.000e+00'),
                ('0=#2.3r', '000.000e+00'),
                ('0=2!3', '000.00'),
                ('0=2!3f', '000.00'),
                ('0=2!3e', '000.00e+00'),
                ('0=2!3r', '000.00e+00'),
                ('0=#2!3r', '000.00e+00')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_non_finite(self):
        cases_list = [
            (float('nan'), [
                ('', 'nan'),
                ('f', 'nan'),
                ('F', 'NAN'),
                ('E', 'NAN'),
                ('%', '(nan)%')
            ]),
            (float('inf'), [
                ('', 'inf'),
                ('f', 'inf'),
                ('F', 'INF'),
                ('E', 'INF')
            ]),
            (float('-inf'), [
                ('', '-inf'),
                ('f', '-inf'),
                ('F', '-INF'),
                ('E', '-INF')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_non_finite_with_exp(self):
        cases_list = [
            (float('nan'), [
                ('', 'nan'),
                ('e', '(nan)e+00'),
                ('E', '(NAN)E+00'),
                ('b', '(nan)b+00'),
                ('B', '(NAN)B+00')
            ]),
            (float('inf'), [
                ('', 'inf'),
                ('e', '(inf)e+00'),
                ('E', '(INF)E+00'),
                ('b', '(inf)b+00'),
                ('B', '(INF)B+00')
            ]),
            (float('-inf'), [
                ('', '-inf'),
                ('e', '(-inf)e+00'),
                ('E', '(-INF)E+00'),
                ('b', '(-inf)b+00'),
                ('B', '(-INF)B+00')
            ])
        ]

        with GlobalDefaultsContext(nan_inf_exp=True):
            self.run_float_fsml_cases(cases_list)

    def test_separators(self):
        cases_list = [
            (123456.654321, [
                ('', '123456.654321'),
                (',', '123,456.654321'),
                (',.s', '123,456.654 321'),
                (',._', '123,456.654_321'),
                ('_._', '123_456.654_321'),
                ('s.s', '123 456.654 321'),
                ('n,n', '123456,654321'),
                ('.,', '123.456,654321'),
                ('.,s', '123.456,654 321'),
                ('.,_', '123.456,654_321'),
                ('_,_', '123_456,654_321'),
                ('s,s', '123 456,654 321')
            ]),
            (12345.54321, [
                ('', '12345.54321'),
                (',', '12,345.54321'),
                (',.s', '12,345.543 21'),
                (',._', '12,345.543_21'),
                ('_._', '12_345.543_21'),
                ('s.s', '12 345.543 21'),
                ('n,n', '12345,54321'),
                ('.,', '12.345,54321'),
                ('.,s', '12.345,543 21'),
                ('.,_', '12.345,543_21'),
                ('_,_', '12_345,543_21'),
                ('s,s', '12 345,543 21')
            ]),
            (1234567.7654321, [
                ('', '1234567.7654321'),
                (',', '1,234,567.7654321'),
                (',.s', '1,234,567.765 432 1'),
                (',._', '1,234,567.765_432_1'),
                ('_._', '1_234_567.765_432_1'),
                ('s.s', '1 234 567.765 432 1'),
                ('n,n', '1234567,7654321'),
                ('.,', '1.234.567,7654321'),
                ('.,s', '1.234.567,765 432 1'),
                ('.,_', '1.234.567,765_432_1'),
                ('_,_', '1_234_567,765_432_1'),
                ('s,s', '1 234 567,765 432 1')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_signs(self):
        cases_list = [
            (+1, [
                ('', '1'),
                ('-', '1'),
                ('+', '+1'),
                (' ', ' 1')
            ]),
            (-1, [
                ('', '-1'),
                ('-', '-1'),
                ('+', '-1'),
                (' ', '-1')
            ]),
            (+0.0, [
                ('', '0'),
                ('-', '0'),
                ('+', '+0'),
                (' ', ' 0')
            ]),
            (-0.0, [
                ('', '0'),
                ('-', '0'),
                ('+', '+0'),
                (' ', ' 0')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_capitalization(self):
        cases_list = [
            (16180.33, [
                ('e', '1.618033e+04'),
                ('E', '1.618033E+04'),
                ('r', '16.18033e+03'),
                ('R', '16.18033E+03')
            ]),
            (1024, [
                ('!3b', '1.00b+10'),
                ('!3B', '1.00B+10')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_padding(self):
        cases_list = [
            (12, [
                ('', '12'),
                ('4', '   12'),
                ('4!3e', '    1.20e+01'),
                (' =4', '   12'),
                (' =4!3e', '    1.20e+01'),
                ('0=4', '00012'),
                ('0=4!3e', '00001.20e+01')
            ])
        ]

        self.run_float_fsml_cases(cases_list)

    def test_prefix(self):
        cases_list = [
            (3.1415e-30, [('ep', '3.1415 q')]),
            (3.1415e-29, [('ep', '3.1415e-29')]),
            (3.1415e-28, [('ep', '3.1415e-28')]),
            (3.1415e-27, [('ep', '3.1415 r')]),
            (3.1415e-26, [('ep', '3.1415e-26')]),
            (3.1415e-25, [('ep', '3.1415e-25')]),
            (3.1415e-24, [('ep', '3.1415 y')]),
            (3.1415e-23, [('ep', '3.1415e-23')]),
            (3.1415e-22, [('ep', '3.1415e-22')]),
            (3.1415e-21, [('ep', '3.1415 z')]),
            (3.1415e-20, [('ep', '3.1415e-20')]),
            (3.1415e-19, [('ep', '3.1415e-19')]),
            (3.1415e-18, [('ep', '3.1415 a')]),
            (3.1415e-17, [('ep', '3.1415e-17')]),
            (3.1415e-16, [('ep', '3.1415e-16')]),
            (3.1415e-15, [('ep', '3.1415 f')]),
            (3.1415e-14, [('ep', '3.1415e-14')]),
            (3.1415e-13, [('ep', '3.1415e-13')]),
            (3.1415e-12, [('ep', '3.1415 p')]),
            (3.1415e-11, [('ep', '3.1415e-11')]),
            (3.1415e-10, [('ep', '3.1415e-10')]),
            (3.1415e-9, [('ep', '3.1415 n')]),
            (3.1415e-8, [('ep', '3.1415e-08')]),
            (3.1415e-7, [('ep', '3.1415e-07')]),
            (3.1415e-6, [('ep', '3.1415 μ')]),
            (3.1415e-5, [('ep', '3.1415e-05')]),
            (3.1415e-4, [('ep', '3.1415e-04')]),
            (3.1415e-3, [('ep', '3.1415 m')]),
            (3.1415e-2, [('ep', '3.1415e-02')]),
            (3.1415e-1, [('ep', '3.1415e-01')]),
            (3.1415e+0, [('ep', '3.1415')]),
            (3.1415e+1, [('ep', '3.1415e+01')]),
            (3.1415e+2, [('ep', '3.1415e+02')]),
            (3.1415e+3, [('ep', '3.1415 k')]),
            (3.1415e+4, [('ep', '3.1415e+04')]),
            (3.1415e+5, [('ep', '3.1415e+05')]),
            (3.1415e+6, [('ep', '3.1415 M')]),
            (3.1415e+7, [('ep', '3.1415e+07')]),
            (3.1415e+8, [('ep', '3.1415e+08')]),
            (3.1415e+9, [('ep', '3.1415 G')]),
            (3.1415e+10, [('ep', '3.1415e+10')]),
            (3.1415e+11, [('ep', '3.1415e+11')]),
            (3.1415e+12, [('ep', '3.1415 T')]),
            (3.1415e+13, [('ep', '3.1415e+13')]),
            (3.1415e+14, [('ep', '3.1415e+14')]),
            (3.1415e+15, [('ep', '3.1415 P')]),
            (3.1415e+16, [('ep', '3.1415e+16')]),
            (3.1415e+17, [('ep', '3.1415e+17')]),
            (3.1415e+18, [('ep', '3.1415 E')]),
            (3.1415e+19, [('ep', '3.1415e+19')]),
            (3.1415e+20, [('ep', '3.1415e+20')]),
            (3.1415e+21, [('ep', '3.1415 Z')]),
            (3.1415e+22, [('ep', '3.1415e+22')]),
            (3.1415e+23, [('ep', '3.1415e+23')]),
            (3.1415e+24, [('ep', '3.1415 Y')]),
            (3.1415e+25, [('ep', '3.1415e+25')]),
            (3.1415e+26, [('ep', '3.1415e+26')]),
            (3.1415e+27, [('ep', '3.1415 R')]),
            (3.1415e+28, [('ep', '3.1415e+28')]),
            (3.1415e+29, [('ep', '3.1415e+29')]),
            (3.1415e+30, [('ep', '3.1415 Q')]),
        ]

        self.run_float_fsml_cases(cases_list)


if __name__ == "__main__":
    unittest.main()
