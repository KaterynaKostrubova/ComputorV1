from typing import List, Iterable, Dict

WHITESPACE_SYMBOLS = "\\t\\r\\n\\f\\v "
FREE_COEFFICIENT_POWER = -1


class NegativePower(Exception):
    pass


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, equation: str, debug: bool = False):
        self.equation = self._prepare(equation)
        self._data = []
        self.debug = debug

    @property
    def data(self):
        return self._data

    @staticmethod
    def _prepare(equation: str) -> str:
        return ''.join(list(filter(lambda x: x not in WHITESPACE_SYMBOLS, equation.lower())))

    def run(self):
        left, right = self.equation.split('=')
        if self.debug:
            print('------------------------------------------------------')
            print('Left part:', left, '\nRight part:', right)
            print('------------------------------------------------------')

        left_data = self.split_by_operator(left)
        right_data = self.split_by_operator(right)
        if self.debug:
            print('Parsed left part:', left_data, '\nParsed right part:', right_data)
            print('------------------------------------------------------')
        left_coefs = self.get_coefficients(left_data)
        right_coefs = {}
        if right_data != ['0']:
            right_coefs = self.get_coefficients(right_data)
        if self.debug:
            print('Left coefficients:', left_coefs, '\nRight coefficients:', right_coefs)
            print('------------------------------------------------------')
        res_coefs = self.simplify(left_coefs, right_coefs)
        if self.debug:
            print('Reduced coefficients:', res_coefs)
            print('------------------------------------------------------')
        return res_coefs

    @staticmethod
    def simplify(left: Dict[int, float], right: Dict[int, float]) -> Dict[int, float]:
        result = left
        for k, v in right.items():
            if k in left:
                result[k] = left[k] - right[k]
            else:
                result[k] = -right[k]
        return result

    def get_coefficients(self, data: List[str]) -> Dict[int, float]:
        result = {}
        for el in data:
            if 'x' not in el:
                self._add_to_result(result, FREE_COEFFICIENT_POWER, float(el))
            elif '*' in el:
                self._split_by('*', result, el)
            else:
                self._split_by('x', result, el)
        return result

    def _split_by(self, operator, result, el):
        coef, unknown = el.split(operator)
        if coef == '+' or coef == '':
            coef = 1
        elif coef == '-':
            coef = -1
        if '^' in unknown:
            power = int(unknown.split('^')[1])
            self._add_to_result(result, power, float(coef))
        else:
            self._add_to_result(result, 1, float(coef))

    @staticmethod
    def _add_to_result(result: dict, power: int, coef: float):
        if power in result:
            result[power] += coef
        else:
            result[power] = coef

    @staticmethod
    def split_by_operator(data: str, operators: Iterable[str] = ('-', '+')) -> List[str]:
        result = []
        part = ''
        last_char_index = len(data) - 1

        for index, char in enumerate(data):
            if char not in operators:
                part += char
            else:
                if data[index - 1] == '^':
                    raise NegativePower
                if part:
                    result.append(part)
                    part = char
                elif char in operators:
                    part = char
            if index == last_char_index:
                result.append(part)
        return result
