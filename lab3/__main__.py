from ..lab2 import Mparser  # noqa
from . import TreePrinter  # noqa
import sys
import os.path

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else \
            os.path.join(os.path.dirname(__file__), 'examples', 'example1.m')
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.lexer)
    ast.printTree()
