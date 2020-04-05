from unittest import TestCase, main
from app import Equation


CASES = {
    '1*x^2=0': (0, None),
    '-1 * x^2 = 0': (0, None),
    'X = 0': (0, None),
    '4 * X = 0': (0, None),
    '1 * X^3 = 0': None,
    '0*x^2=0': (None, None),
    '5 * X^0 = 5 * X^0': (None, None),
    '4 * X^0 = 8 * x^0': (None, None),
    '5 * X^0 = 4 * X^0 + 7 * X^1': (0.14, None),
    '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0': (-0.48, 0.91),
    '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 5 * X^0 + 4 * X^1 - 9.3 * X^2': (None,  None),
    '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 5 * X^0 + 4 * X^1 + 9.3 * X^2': (0,  None),
    '5 * X^0 + 13 * X^1 + 3 * X^2 = 1 * X^0 + 1 * X^1': (-0.37, -3.63),
    '6 * X^0 + 11 * X^1 + 5 * X^2 = 1 * X^0 + 1 * X^1': (-1, None),
    '5 * X^0 + 3 * X^1 + 3 * X^2 = 1 * X^0 + 0 * X^1': ('-0.5 + 1.04i', '-0.5 - 1.04i'),
    '1 * X ^ 2 + 3 * X^1 + 15 = 2 * X ^ 2 + 4 * X^1 - 10': (-5.52, 4.52),
    'X^2 + 3X + 15 = 2 * X ^ 2 + 4 * X^1 - 10': (-5.52, 4.52),
    '1 X ^ 2 + 2 X ^ 2 + X + 15 + 3 X ^ 2 + 5 X + 30 = 0': ('-0.5 + 2.69i', '-0.5 - 2.69i'),
    '6X^2 -6x + 1.5 = 0': (0.5, None),
    '7x^2 - 4x - 5 = -2* x^1 + 1 - 1': (1, -0.71),
    '36x^2 + 1 = 0*x^1': ('0.0 + 0.17i', '0.0 - 0.17i'),
    '5 * x^0 = 8': (None, None),
    '5 * X^-0 + 4 * X^-1 - 9.3 * X^2 = 0': None,
    '5                   * X												^0 + 4': None,
    # "5^0 + x = 0"
#     5x^0 = 0" // + 5 = 0

}


class TestComputor(TestCase):
    def test_all(self):
        for equation, expected_result in CASES.items():
            print('Equation ---> ', equation, ':')
            eq = Equation(equation)
            result = eq.run()
            self.assertEqual(result, expected_result)
            print('---------------------------------------------------')

if __name__ == '__main__':
    main()
