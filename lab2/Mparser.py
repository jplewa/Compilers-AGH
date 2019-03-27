import lab1.scanner as scanner
import ply.yacc as yacc
import sys
sys.path.append("..")


tokens = scanner.tokens

precedence = (
    # to fill ...
    # ("left", 'ADD', 'SUB'),
    # ('left', '\'[\'')
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


def p_instructions(p):
    """ instructions : instructions instruction ';'
                     | instructions BREAK ';'
                     | instructions PRINT print ';'
                     | instructions CONTINUE ';'
                     | instructions flow
                     | instructions RETURN argument ';'
                     | instructions block
                     | instruction ';'
                     | BREAK ';'
                     | CONTINUE ';'
                     | PRINT print ';'
                     | flow
                     | block
                     | RETURN argument ';'"""


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


def p_conditional_expressions(p):
    """ conditional_expressions : if conditional_expressions
                                | if else_if 
                                | if """


def p_else_if(p):
    """ else_if : ELSE if else_if 
                | ELSE if
                | ELSE one_liners
                | ELSE block """


def p_if(p):
    """ if : IF '(' condition ')' one_liners 
           | IF '(' condition ')' block """


def p_block(p):
    """ block : '{' instructions '}'"""


def p_number_instruction(p):
    """number_instruction : signed_number ADD xd
                          | signed_number SUB xd
                          | signed_number MUL xd
                          | signed_number DIV xd """


def p_xd(p):
    """xd : number
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
    """ ARRAY : '[' vector ']' 
              | index """


def p_array(p):
    """ array : ARRAY
              | assignable """


def p_vector(p):
    """ vector : '[' vector ']'
               | index
               | vector ',' vectors """


def p_vectors(p):
    """ vectors :  index
                | '[' vectors ']' """


def p_index(p):
    """ index : '[' indices intnum ']'
              | '[' intnum ']' """


def p_indices(p):
    """ indices : indices ',' intnum
                | intnum ',' """


def p_assignable(p):
    """ assignable : ID 
                   | ID index """


parser = yacc.yacc()
