import sys
import ply.yacc as yacc  # noqa
from ..lab2 import Mparser  # noqa
from ..lab3 import TreePrinter  # noqa
from ..lab4 import TypeChecker  # noqa
from . import Interpreter  # noqa
import os.path


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else \
            os.path.join(os.path.dirname(__file__), 'examples', 'example1.m')
        file = open(filename, "r")
    except IOError:
        print(f'Cannot open {filename} file')
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.lexer)

    if ast is None:
        exit()

    # Below code shows how to use visitor
    error = TypeChecker.TypeChecker().visit(ast)   # or alternatively ast.accept(typeChecker)

    if not error:
        ast.accept(Interpreter.Interpreter())

    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
