#!/usr/bin/python3

import sys
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
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACES',
    'RBRACES',
    'NUMBER',
    'MATRIX_PLUS',
    'MATRIX_MINUS',
    'MATRIX_TIMES',
    'MATRIX_DIVIDE',
    'ASSIGN',
    'PLUS_ASSIIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'LT',
    'GT',
    'LEQ',
    'GEQ',
    'NEQ',
    'EQ',
    'RANGE',
    'TRANSPOSE',
    'COMMA',
    'SEMICOLON',
    'ID',
) + tuple(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_LBRACES = r'\{'
t_RBRACES = r'\}'

t_MATRIX_PLUS = r'\.\+'
t_MATRIX_MINUS = r'\.-'
t_MATRIX_TIMES = r'\.\*'
t_MATRIX_DIVIDE = r'\./'

t_ASSIGN = r'='
t_PLUS_ASSIIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='

t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'='

t_RANGE = r':'

t_TRANSPOSE = r'\''

t_COMMA = r','
t_SEMICOLON = r';'

t_ignore = ' \t'


def t_NUMBER(t):
    # r'\d+'
    r'\d+(\.\d+)? ((E|e) (+|–)? cyfra + )?'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "plik.ini", "r")
    lexer.input(fh.read())
    print(lexer)
    for token in lexer:
        print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
        print(token)
except:
    print("open error\n")
