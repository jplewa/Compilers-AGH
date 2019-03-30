import lab1.scanner as scanner
import ply.yacc as yacc
import sys
sys.path.append("..")


tokens = scanner.tokens

precedence = (
    # to fill ...
    ("left", 'ADD', 'SUB'),
    ("left", 'DIV', 'MUL'),
    ("nonassoc", 'NO_ELSE', 'NO_INDEX'),
    ("nonassoc", 'ELSE', '[')
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


def p_instructions_opt(p):
    """instructions_opt : instructions
                        | """

def p_comment_opt(p):
    """ comment_opt : COMMENT
                    | """


def p_instructions(p):
    """ instructions : instructions instruction ';' comment_opt
                     | instructions BREAK ';' comment_opt
                     | instructions PRINT print ';' comment_opt
                     | instructions CONTINUE ';' comment_opt
                     | instructions flow comment_opt
                     | instructions RETURN argument ';' comment_opt
                     | instructions block comment_opt
                     | instruction ';' comment_opt
                     | BREAK ';' comment_opt
                     | CONTINUE ';' comment_opt
                     | PRINT print ';' comment_opt
                     | flow comment_opt
                     | block comment_opt
                     | RETURN argument ';' comment_opt"""


def p_print(p):
    """ print : argument ',' print
              | argument """


def p_flow(p):
    """ flow : while_loop
             | for_loop
             | conditional_expressions """


def p_assignment(p):
    """assignment : assignable '=' argument
                  | assignable ADDASSIGN argument
                  | assignable SUBASSIGN argument
                  | assignable DIVASSIGN argument
                  | assignable MULASSIGN argument """


def p_argument(p):
    """ argument : SIGNED_NUMBER
                 | STRING
                 | ARRAY
                 | instruction
                 | assignable """


def p_instruction(p):
    """ instruction : number_instruction
                    | matrix_instruction
                    | assignment
                    | function """


def p_condition(p):
    """ condition : argument EQ argument 
                  | argument NEQ argument
                  | argument LEQ argument
                  | argument GEQ argument
                  | argument LT argument
                  | argument GT argument """


def p_while_loop(p):
    """ while_loop : WHILE '(' condition ')' inner_loop """


def p_for_loop(p):
    """ for_loop : FOR ID '=' number ':' number inner_loop """


def p_inner_loop(p):
    """ inner_loop : one_liners
                   | conditional_expressions
                   | block """


def p_one_liners(p):
    """ one_liners : PRINT print ';'
                   | BREAK ';'
                   | CONTINUE ';'
                   | RETURN argument ';'
                   | instruction ';'
                   | while_loop
                   | for_loop """

def p_if_body(p):
    """ if_body : one_liners
                | block
                | conditional_expressions"""

def p_conditional_expressions(p):
    """ conditional_expressions : if"""

def p_if(p):
    """ if : IF '(' condition ')' if_body %prec NO_ELSE
           | IF '(' condition ')' if_body ELSE if_body"""

# def p_else_if(p):
#     """ else_if : ELSE if else_if 
#                 | ELSE if
#                 | ELSE one_liners
#                 | ELSE block """


# def p_if(p):
#     """ if : IF '(' condition ')' one_liners 
#            | IF '(' condition ')' block """




def p_block(p):
    """ block : '{' instructions '}'"""


def p_number_instruction(p):
    """number_instruction : signed_number ADD arithmetic_operand
                          | signed_number SUB arithmetic_operand
                          | signed_number MUL arithmetic_operand
                          | signed_number DIV arithmetic_operand """


def p_arithmetic_operand(p):
    """arithmetic_operand : number
                          | number_instruction """


def p_SIGNED_NUMBER(p):
    """SIGNED_NUMBER : SUB NUMBER
                     | SUB assignable
                     | NUMBER """


def p_signed_number(p):
    """signed_number : SUB number
                     | number """


def p_matrix_instruction(p):
    """matrix_instruction : array DOTADD array
                          | array DOTSUB array
                          | array DOTMUL array
                          | array DOTDIV array 
                          | array "'" """


def p_function(p):
    """function : ZEROS '(' intnum ')'
                | ONES '(' intnum ')'
                | EYE '(' intnum ')'"""


def p_intnum(p):
    """ intnum : INTNUM
               | assignable """

# def p_float(p):
#     """ float : FLOAT
#               | assignable """

# def p_string(p):
#     """ string : STRING
#                | assignable """


def p_NUMBER(p):
    """ NUMBER : INTNUM 
               | FLOAT"""


def p_number(p):
    """ number : INTNUM 
               | FLOAT 
               | assignable  """


def p_ARRAY(p):
    """ ARRAY : vector """


def p_array(p):
    """ array : ARRAY
              | assignable """


# def p_vector(p):
#     """ vector : '[' vector ']'
#                | index
#                | vector ',' vectors """


# def p_vectors(p):
#     """ vectors :  index
#                 | '[' vectors ']' """

def p_vector(p):
    """ vector : index
               | '[' vector_list ']'"""

def p_vector_list(p):
    """ vector_list : vector_list ',' vector
                    | vector """


def p_index(p):
    """ index : '[' index_list ']' """


def p_index_list(p):
    """ index_list : index_list ',' intnum
                | intnum """


def p_assignable(p):
    """ assignable : ID index 
                   | ID %prec NO_INDEX"""


parser = yacc.yacc()
