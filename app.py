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
        # self.coefficients = self._parse()

    @property
    def power(self) -> int:
        return max(list(self.coefficients.keys()))

    def reduce(self, degrees: dict = None, simplified: bool = False) -> str:
        tpl = []

        coefs = degrees or self.coefficients
        degrees = list(coefs.keys())

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
        #
        # if FREE_COEFFICIENT_POWER in degrees:
        #     degrees = degrees[1:] + [degrees[0]]

        for i, degree in enumerate(degrees):
            tpl_v = '{}{}x{}'
            coef = coefs[degree]

            if degree == FREE_COEFFICIENT_POWER:
                degree = ''
                tpl_v = '{}{}{}'

            if simplified and degree == 0:
                degree = ''
                tpl_v = '{}{}{}'

            if degree == 1:
                degree = ''
                # tpl_v = '{}{}x{}'

            if get_absolute(int(coef)) == 1:
                coef = ''

            if coef != '' and coef < 0:
                sign = '-' if i == 0 else '- '
                coef = -coef
            else:
                sign = '' if i == 0 else '+ '

            if coef != 0:
                if str(degree) in powers:
                    v = tpl_v.format(sign, coef, powers[str(degree)])
                    tpl.append(v)
                else:
                    d2 = ''
                    for index, char in enumerate(str(degree)):
                        d2 = d2+powers[char]
                    v = tpl_v.format(sign, coef, d2)
                    tpl.append(v)

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

        return res

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
        c = self.coefficients.get(-1, 0) + self.coefficients.get(0, 0)
        res = self._solve(a, b, c)
        return res

    def _solve(self, a, b, c):
        if a == 0:
            return self._solve_simple(b, c)
        discriminant = b ** 2 - 4 * a * c
        if self.more:
            print("Discriminant:", discriminant)
        if discriminant > 0:
            x1 = round((-b + sqrt(discriminant)) / (2 * a), 2)
            x2 = round((-b - sqrt(discriminant)) / (2 * a), 2)
            print("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(x1, x2))

        elif discriminant < 0:
            x1, x2 = self.find_complex_solutions(a, b, discriminant)
            print("Discriminant is strictly negative, the two complex solutions are:\n{}\n{}".format(x1, x2))
        else:
            x1 = round((-b + sqrt(discriminant)) / (2 * a), 2) or 0
            x2 = None
            print("Discriminant is equal to zero, the solution is:\n{}".format(x1))

        return x1, x2

    def _solve_simple(self, b, c):
        result = None
        reduced = self.reduce({FREE_COEFFICIENT_POWER: c, 1: b}, simplified=True)

        if b == 0 and c:
            print('Unsolvable equation: {}'.format(reduced))
            return result, None

        if b == 0:
            print('All real numbers are solutions!')
            return result, None

        result = round(-c / b, 2)

        # print('Simplified: {}'.format(reduced))
        print('Solution: {}'.format(result))
        return result, None

    def run(self):
        try:
            self.coefficients = self._parse()
        except NegativePower:
            print('Oops.. invalid power, I can\'t solve this equation. Try another!')
            return
        except Exception as err:
            if self.debug:
                print('PARSING_ERROR:', err)
            print('Oops, that was no valid equation... Try another!')
            return
        print('Reduced form:', self.reduce())
        print('Polynomial degree:', max(self.power, 0))
        if self.power > 2:
            print('The polynomial degree is strictly greater than 2, I can\'t solve.')
        else:
            return self.solve()

# if __name__ == '__main__':
#     Equation("2*x^0-1=-3.2").run()
