from ..lab1 import scanner  # pylint: disable=relative-beyond-top-level
from . import Mparser
import sys
import os.path

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else \
            os.path.join(os.path.dirname(__file__), 'examples', 'example1.m')
        file = open(filename, 'r')
    except IOError:
        print(f'Cannot open {filename} file')
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
