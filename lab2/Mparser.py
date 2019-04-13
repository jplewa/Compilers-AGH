import sys
sys.path.append("..")

import ply.yacc as yacc
import lab3.AST as AST
import lab1.scanner as scanner

lexer = scanner.lexer
tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IF'),
    ("nonassoc", 'ELSE'),
    ("right", '='),
    ("nonassoc", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
    ("nonassoc", 'LT', 'GT', "LEQ", "GEQ", "EQ", "NEQ"),
    ("left", 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
    ("left",  'MUL', 'DIV', "DOTMUL", "DOTDIV"),
    ("left", '\''),
    ("right", 'NEGATIVE'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")

addInstruction
def p_program(p):
    """ program : instructions
                |
    """
    if len(p) == 2:
        p[0] = AST.Program(p[1])
    else:
        p[0] = AST.Program()


def p_instructions(p):
    """ instructions : instructions instruction
                     | instruction
    """
    if len(p) == 2:
        
        p[0] = AST.Instructions(p[1])
    else:
        p[0] = AST.Instructions(p[1])
        p[0].addInstruction(p[2])

def p_instruction(p):
    """ instruction : return
                    | break
                    | continue
                    | print
    """


def p_assignment_instruction(p):
    """ instruction : variable '=' expression ';'
                    | variable '=' error ';'
    """

def p_arithmetic_assignment_instruction(p):
    """ instruction : variable ADDASSIGN expression ';'
                    | variable SUBASSIGN expression ';'
                    | variable DIVASSIGN expression ';'
                    | variable MULASSIGN expression ';'
    """


def p_variable(p):
    """ variable : ID
                 | ID element_list
    """


def p_return(p):
    """ return : RETURN expression ';' """


def p_break(p):
    """ break : BREAK ';' """


def p_continue(p):
    """ continue : CONTINUE ';' """


def p_value_expression(p):
    """ expression : INTNUM
                   | STRING
                   | FLOAT
    """


def p_id_expression(p):
    """ expression : ID """


def p_arithmetic_expression(p):
    """ expression : expression ADD expression
                   | expression SUB expression
                   | expression DIV expression
                   | expression MUL expression
    """
    p[0] = AST.BinExpr(p[1], p[2], p[3])


def p_matrix_expression(p):
    """ expression : expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression
    """


def p_relational_expression(p):
    """ condition : expression EQ expression
                  | expression NEQ expression
                  | expression GEQ expression
                  | expression LEQ expression
                  | expression GT expression
                  | expression LT expression
    """


def p_negation_expression(p):
    """ expression : SUB expression %prec NEGATIVE """


def p_transposition_expression(p):
    """ expression : expression "'" """


def p_functional_expression(p):
    """ expression : ZEROS '(' expression ')'
                   | ONES '(' expression ')'
                   | EYE '(' expression ')'
    """


def p_list(p):
    """ expression : '[' element_list ']' """


def p_element_list(p):
    """ element_list : expression ',' element_list
                     | expression
    """


def p_print(p):
    """ print : PRINT element_list ';' """


def p_if_instruction(p):
    """ instruction : IF '(' condition ')' instruction %prec IF
                    | IF '(' condition ')' instruction ELSE instruction
                    | IF '(' error ')' instruction %prec IF
                    | IF '(' error ')' instruction ELSE instruction
    """


def p_while_instruction(p):
    """ instruction : WHILE '(' condition ')' instruction
                    | WHILE '(' error ')' instruction
    """


def p_for_instruction(p):
    """ instruction : FOR variable '=' expression ':' expression instruction
                    | FOR variable '=' error ':' expression instruction
                    | FOR variable '=' expression ':' error instruction
    """


def p_compound_instruction(p):
    """ instruction : '{' instructions '}' """

parser = yacc.yacc()
