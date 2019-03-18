#!/usr/bin/python
import ply.yacc as yacc
import lab1.scanner as scanner
import sys
sys.path.append("..")


tokens = scanner.tokens

precedence = (
    # to fill ...
    ("left", 'ADD', 'SUB'),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(
            p.lineno, scanner.find_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction ';' """


def p_instructions_2(p):
    """instructions : instruction ';' """


def p_instruction_1(p):
    """instruction : number ADD number 
                   | number SUB number
                   | number MUL number
                   | number DIV number"""
                   

def p_instruction_2(p):
    """instruction : ID '=' instruction """

def p_instruction_3(p):
    """instruction : ZEROS '(' INTNUM ')' 
                   | ONES '(' INTNUM ')' 
                   | EYE '(' INTNUM ')'"""


def p_number(p):
    """ number : INTNUM 
               | FLOAT"""
def p_index(p):
    """ index : '[' indices INTNUM ']'"""

def p_indices(p):
    

def p_assignable(p):
    """ assignable : ID
                   | ID index """


parser = yacc.yacc()
