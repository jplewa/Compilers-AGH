import ply.lex as lex

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
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
    'ASSIGN',
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
    'STRING',
    'COMMENT',
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

t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'


def t_FLOAT(t):
    r'(\d+(\.\d*)|(\.\d+))((E|e)(\+|–)?\d+)?'
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
    r'(".*")|(\'.*\')'
    t.value = str(t.value)
    return t


def t_COMMENT(t):
    r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()


def find_column(text, tok):
    text = text.split('\n')
    pos = 0
    for line in text:
        if pos + len(line) > tok.lexpos:
            return tok.lexpos - pos + 1
        pos += len(line) + 1
    raise ValueError('Column not found')
