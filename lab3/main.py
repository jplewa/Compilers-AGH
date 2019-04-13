import sys
sys.path.append("..")
import lab2.Mparser as Mparser
import ply.yacc as yacc
from TreePrinter import TreePrinter



if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.lexer)
    ast.printTree()
