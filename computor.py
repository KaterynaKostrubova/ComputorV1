from argparse import ArgumentParser

from app import Equation


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('equation')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--more', action='store_true')
    args = parser.parse_args()

    Equation(args.equation, args.debug, args.more).run()
