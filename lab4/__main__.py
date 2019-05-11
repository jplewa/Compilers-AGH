import sys
import ply.yacc as yacc # noqa
from ..lab2 import Mparser  # noqa
from ..lab3 import TreePrinter  # noqa
from . import TypeChecker
import os.path

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else \
            os.path.join(os.path.dirname(__file__), 'examples', '1.m')
        file = open(filename, 'r')
    except IOError:
        print(f'Cannot open {filename} file')
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker.TypeChecker()
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    print()
    print("--------SYMBOLS--------")
    typeChecker.symbol_table.prettyPrint()
