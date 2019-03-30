import lab1.scanner as scanner
import ply.yacc as yacc
import sys
sys.path.append("..")


tokens = scanner.tokens

precedence = (
    ("left", 'ADD', 'SUB'),
    ("left", 'DIV', 'MUL'),
    # ("left", 'EQ', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT'),
    ("left", '='), #'DIVASSIGN', 'MULASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ("nonassoc", 'NO_ELSE', 'NO_INDEX'),
    ("nonassoc", 'ELSE', '[')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """ program : instructions_opt """


def p_instructions_opt(p):
    """ instructions_opt : instructions
                         |
    """


def p_comment_opt(p):
    """ comment_opt : COMMENT
                    |
    """


def p_instructions(p):
    """ instructions : instructions single_instruction comment_opt
                     | single_instruction comment_opt
    """


def p_single_instruction(p):
    """ single_instruction : BREAK ';'
                           | CONTINUE ';'
                           | PRINT element_list ';'
                           | RETURN instruction ';'
                           | flow
                           | block
                           | instruction ';'
    """


def p_element_list(p):
    """ element_list : instruction ',' element_list
                     | instruction
    """


def p_flow(p):
    """ flow : while_loop
             | for_loop
             | if
    """


def p_instruction(p):
    """ instruction : conditional_operand
                    | CONDITION
    """


def p_assignment(p):
    """ assignment : assignable '=' instruction """


def p_arithmetic_assignment(p):
    """ arithmetic_assignment : assignable ADDASSIGN signed_number
                              | assignable SUBASSIGN signed_number
                              | assignable DIVASSIGN signed_number
                              | assignable MULASSIGN signed_number
    """


def p_CONDITION(p):
    """ CONDITION : instruction EQ conditional_operand
                  | instruction NEQ conditional_operand
                  | instruction LEQ conditional_operand
                  | instruction GEQ conditional_operand
                  | instruction LT conditional_operand
                  | instruction GT conditional_operand
    """


def p_conditional_operand(p):
    """ conditional_operand : STRING
                            | arithmetic_assignment
                            | number_instruction
                            | SIGNED_NUMBER
                            | matrix_instruction
                            | ARRAY
                            | function
                            | assignment
                            | assignable
    """


def p_condition(p):
    """ condition : CONDITION
                  | assignable
    """


def p_while_loop(p):
    """ while_loop : WHILE '(' condition ')' single_instruction """


def p_for_loop(p):
    """ for_loop : FOR ID '=' number ':' number single_instruction """


def p_if(p):
    """ if : IF '(' condition ')' single_instruction %prec NO_ELSE
           | IF '(' condition ')' single_instruction ELSE single_instruction
    """


def p_block(p):
    """ block : '{' instructions '}'
              | '{' '}'
    """


def p_number_instruction(p):
    """ number_instruction : signed_number ADD arithmetic_operand
                           | signed_number SUB arithmetic_operand
                           | signed_number MUL arithmetic_operand
                           | signed_number DIV arithmetic_operand
    """


def p_arithmetic_operand(p):
    """ arithmetic_operand : number_instruction
                           | number
    """


def p_SIGNED_NUMBER(p):
    """ SIGNED_NUMBER : SUB NUMBER
                      | SUB assignable
                      | NUMBER
    """


def p_signed_number(p):
    """ signed_number : SUB number
                      | number
    """


def p_matrix_instruction(p):
    """ matrix_instruction : array DOTADD matrix_operand
                           | array DOTSUB matrix_operand
                           | array DOTMUL matrix_operand
                           | array DOTDIV matrix_operand
    """


def p_matrix_operand(p):
    """ matrix_operand : array
                       | matrix_instruction
    """


def p_function(p):
    """ function : ZEROS '(' intnum ')'
                 | ONES '(' intnum ')'
                 | EYE '(' intnum ')'
    """


def p_intnum(p):
    """ intnum : INTNUM
               | assignable
    """


def p_NUMBER(p):
    """ NUMBER : INTNUM
               | FLOAT
    """


def p_number(p):
    """ number : INTNUM
               | FLOAT
               | assignable
    """


def p_array(p):
    """ array : ARRAY
              | assignable
    """


def p_ARRAY(p):
    """ ARRAY : '[' element_list ']'
              | '[' element_list ']' "'"
              | assignable "'"
    """


def p_index(p):
    """ index : '[' index_list ']' """


def p_index_list(p):
    """ index_list : index_list ',' intnum
                   | intnum
    """


def p_assignable(p):
    """ assignable : ID index
                   | ID %prec NO_INDEX"""


parser = yacc.yacc()
