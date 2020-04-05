import sys

from austin.cli import get_argument_parser
from austin.main import main
from austin.output import output


if __name__ == '__main__':
    parser = get_argument_parser()
    namespace = parser.parse_args(sys.argv[1:])

    info = main(**vars(namespace))
    output(info)
