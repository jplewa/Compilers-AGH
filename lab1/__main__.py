import sys
from . import scanner
import os.path

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
            os.path.dirname(__file__), 'examples', 'example_full.txt')
        file = open(filename, 'r')
    except IOError:
        print(f'Cannot open {filename} file')
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer
    lexer.input(text)  # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break    # No more input
        column = scanner.find_column(tok)
        print(f'({tok.lineno},{column}): {tok.type}({tok.value})')
