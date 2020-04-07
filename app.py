from parser import Parser, FREE_COEFFICIENT_POWER, NegativePower, ParsingError


def get_absolute(num):
    return num if num >= 0 else -num


def sqrt(num):
    """Finds square root of a given number with a given precision."""
    num = float(num)
    results = {
        0.: 0.,
        1.: 1.,
    }
    if num in results:
        return results[num]
    if num < 0:
        raise Exception('Only positive numbers')
    precision = 9  # more than 9 has no effect
    delta_error = 1 / 10 ** precision
    result = num / 2
    while get_absolute(result ** 2 - num) >= delta_error:
        delta = num / result
        result = (result + delta) / 2
    return result


class Equation:
    def __init__(self, equation: str, debug: bool = False, more: bool = False):
        self._data = equation
        self.debug = debug
        self.more = more
        self.coefficients = {}

    def reduce(self, degrees: dict = None):
        tpl = []
        coefs = degrees or self.coefficients
        coefs[-1] = coefs.get(-1, 0) + coefs.get(0, 0)
        degrees = list(coefs.keys())
        max_degree = 0
        powers = {
            '0': u'\u2070',
            '1': u'\u00B9',
            '2': chr(178),
            '3': chr(179),
            '4': u'\u2074',
            '5': u'\u2075',
            '6': u'\u2076',
            '7': u'\u2077',
            '8': u'\u2078',
            '9': u'\u2079',
        }

        degrees.sort(reverse=True)

        for i, degree in enumerate(degrees):
            tpl_v = '{}{}x{}'
            coef = coefs[degree]
            free = 0

            if degree == FREE_COEFFICIENT_POWER:
                free = 1
                degree = ''
                tpl_v = '{}{}{}'
            elif int(coef) == 1:
                coef = ''

            if degree == 1:
                degree = ''

            if coef != '' and coef < 0:
                sign = '-' if tpl == [] else '- '
                coef = -coef
                if get_absolute(int(coef)) == 1 and not free:
                    coef = ''
            else:
                sign = '' if tpl == [] else '+ '

            if coef != 0 and degree != 0:
                if str(degree) in powers:
                    dgr = powers[str(degree)]
                    v = tpl_v.format(sign, coef, dgr)
                    tpl.append(v)
                else:
                    dgr = ''
                    for index, char in enumerate(str(degree)):
                        dgr = dgr+powers[char]
                    v = tpl_v.format(sign, coef, dgr)
                    tpl.append(v)
                if free:
                    max_degree = max_degree
                elif degree == '':
                    max_degree = 1 if max_degree < 1 else max_degree
                elif max_degree < degree:
                    max_degree = degree
        if tpl:
            tpl += ['= 0']
        else:
            tpl += ['0 = 0']

        res = ' '.join(tpl)

        repl = {
            '.0 ': ' ',
            '.0': '',
        }

        for k, v in repl.items():
            res = res.replace(k, v)
        return res, max_degree

    def _parse(self) -> dict:
        return Parser(self._data, self.debug).run()

    @staticmethod
    def find_complex_solutions(a, b, discriminant):
        b_part = -b
        d_part = sqrt(get_absolute(discriminant))
        a_part = get_absolute(2 * a)
        first = round(b_part / a_part, 2)
        second = round(d_part / a_part, 2)
        x1 = '{} + {}i'.format(first, second)
        x2 = '{} - {}i'.format(first, second)
        return x1, x2

    def solve(self):
        a = self.coefficients.get(2, 0)
        b = self.coefficients.get(1, 0)
        c = self.coefficients.get(-1, 0)
        res = self._solve(a, b, c)
        return res

    def _solve(self, a, b, c):
        if a == 0:
            return self._solve_simple(b, c)
        discriminant = b ** 2 - 4 * a * c
        if self.more:
            print("\033[1;35mDiscriminant:\033[1;33m", discriminant, '')
        if discriminant > 0:
            x1 = round((-b + sqrt(discriminant)) / (2 * a), 2)
            x2 = round((-b - sqrt(discriminant)) / (2 * a), 2)
            print("\033[1;36mDiscriminant is strictly positive, "
                  "the two solutions are:\033[1;32m\n{}\n{}\033[0m".format(x1, x2))

        elif discriminant < 0:
            x1, x2 = self.find_complex_solutions(a, b, discriminant)
            print("\033[1;36mDiscriminant is strictly negative, the two "
                  "complex solutions are:\033[1;32m\n{}\n{}\033[0m".format(x1, x2))
        else:
            x1 = round((-b + sqrt(discriminant)) / (2 * a), 2) or 0
            x2 = None
            print("\033[1;36mDiscriminant is equal to zero, the solution is:\033[1;32m\n{}\033[0m".format(x1))

        return x1, x2

    def _solve_simple(self, b, c):
        result = None
        reduced, power = self.reduce({FREE_COEFFICIENT_POWER: c, 1: b})
        if b == 0 and c:
            print('\033[1;31mUnsolvable equation:\033[1;33m {}\033[0m'.format(reduced))
            return result, None

        if b == 0:
            print('\033[1;32mAll real numbers are solutions!\033[0m')
            return result, None

        result = round(-c / b, 2) or 0
        print('\033[1;32mSolution: {}\033[0m'.format(result))
        return result, None

    def run(self):
        try:
            self.coefficients = self._parse()
        except NegativePower:
            print('\033[1;31mOops.. invalid power, I can\'t solve this equation. Try another!\033[0m')
            return
        except Exception as err:
            if self.debug:
                print('PARSING_ERROR:', err)
            print('\033[1;31mOops, that was no valid equation... Try another!\033[0m')
            return

        try:
            reduce_form, max_power = self.reduce()

            print('\033[1;34mReduced form:\033[1;33m', reduce_form, '\033[0m')
            print('\033[1;34mPolynomial degree:\033[1;33m', max_power, '\033[0m')

            if max_power > 2:
                print('\033[1;31mThe polynomial degree is strictly greater than 2, I can\'t solve.\033[0m')
                return (None, None), reduce_form, max_power
            else:
                return self.solve(), reduce_form, max_power

        except Exception as err:
            print('\033[1;31mOops, something go wrong... Try another equation!\033[0m')
            if self.debug:
                print('SOLVING_ERROR:', err)




# if __name__ == '__main__':
#     Equation("2*x^0-1=-3.2").run()
