import ply.lex as lex   # pylint: disable=useless-import-alias

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

tokens = (
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'LT',
    'GT',
    'LEQ',
    'GEQ',
    'NEQ',
    'EQ',
    'FLOAT',
    'INTNUM',
    'ID',
    'STRING'
) + tuple(reserved.values())

literals = ['=', '(', ')', '{', '}', '[', ']', ';', ',', '\'', ':']

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LEQ = r'<='
t_GEQ = r'>='
t_LT = r'<'
t_GT = r'>'
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'


def t_FLOAT(t):
    r'(\d+(\.\d*)|(\.\d+))((E|e)(\+|-)?\d+)?|(\d+(E|e)(\+|-)?\d+)'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r'(".*?")|(\'.*?\')'
    t.value = str(t.value)[1:-1]    # to skip the quotation marks
    return t


def t_COMMENT(_):
    r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Illegal character at line {t.lineno}, column {find_column(t)}: "{t.value[0]}"')
    t.lexer.skip(1)


lexer = lex.lex()


def find_column(tok):
    split_text = lexer.lexdata.split('\n')
    pos = 0
    for line in split_text:
        if pos + len(line) > tok.lexpos:
            return tok.lexpos - pos + 1
        pos += len(line) + 1
    raise ValueError('Column not found')
