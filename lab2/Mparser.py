import ply.yacc as yacc     # pylint: disable=useless-import-alias
from ..lab3 import AST      # pylint: disable=relative-beyond-top-level
from ..lab1 import scanner  # pylint: disable=relative-beyond-top-level


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
        print(f'Syntax error at line {p.lineno}, column \
            {scanner.find_column(p)}: LexToken({p.type}, "{p.value}"')
    else:
        print('Unexpected end of input')


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
        p[0] = p[1]
        p[0].addInstruction(p[2])


def p_instruction(p):
    """ instruction : return
                    | break
                    | continue
                    | print
    """
    p[0] = p[1]


def p_compound_instruction(p):
    """ instruction : '{' instructions '}' """
    p[0] = p[2]


def p_assignment_instruction(p):
    """ instruction : variable '=' expression ';'
                    | variable '=' error ';'
    """
    p[0] = AST.Assignment(p[2], p[1], p[3])


def p_arithmetic_assignment_instruction(p):
    """ instruction : variable ADDASSIGN expression ';'
                    | variable SUBASSIGN expression ';'
                    | variable DIVASSIGN expression ';'
                    | variable MULASSIGN expression ';'
    """
    p[0] = AST.ArithmeticAssignment(p[2], p[1], p[3])


def p_if_instruction(p):
    """ instruction : IF '(' condition ')' instruction %prec IF
                    | IF '(' condition ')' instruction ELSE instruction
                    | IF '(' error ')' instruction %prec IF
                    | IF '(' error ')' instruction ELSE instruction
    """
    if len(p) == 8:
        p[0] = AST.If(p[1], p[3], p[5], p[6], p[7])
    else:
        p[0] = AST.If(p[1], p[3], p[5])


def p_while_instruction(p):
    """ instruction : WHILE '(' condition ')' instruction
                    | WHILE '(' error ')' instruction
    """
    p[0] = AST.While(p[1], p[3], p[5])


def p_for_instruction(p):
    """ instruction : FOR variable '=' range instruction """
    p[0] = AST.For(p[1], p[2], p[4], p[5])


def p_range(p):
    """ range : expression ':' expression
              | error ':' expression
              | expression ':' error
    """
    p[0] = AST.Range(p[2], p[1], p[3])


def p_variable(p):
    """ variable : ID
                 | ID '[' index_list ']'
    """
    if len(p) == 2:
        p[0] = AST.Variable(p[1])
    else:
        p[0] = AST.Ref(p[1], p[3])


def p_index_list(p):
    """ index_list : index_list ',' variable
                   | index_list ',' INTNUM
                   | variable
                   | INTNUM
    """

    def _eval(x):
        return AST.IntNum(x) if isinstance(x, int) else x

    if len(p) == 2:
        p[0] = AST.IndexList(_eval(p[1]))
    else:
        p[0] = p[1]
        p[0].addIndex(_eval(p[3]))


def p_return(p):
    """ return : RETURN expression ';' """
    p[0] = AST.Return(p[1], p[2])


def p_break(p):
    """ break : BREAK ';' """
    p[0] = AST.Break(p[1])


def p_continue(p):
    """ continue : CONTINUE ';' """
    p[0] = AST.Continue(p[1])


def p_intnum_expression(p):
    """ expression : INTNUM """
    p[0] = AST.IntNum(p[1])


def p_float_expression(p):
    """ expression : FLOAT """
    p[0] = AST.FloatNum(p[1])


def p_string_expression(p):
    """ expression : STRING """
    p[0] = AST.String(p[1])


def p_id_expression(p):
    """ expression : ID """
    p[0] = AST.Variable(p[1])


def p_arithmetic_expression(p):
    """ expression : expression ADD expression
                   | expression SUB expression
                   | expression DIV expression
                   | expression MUL expression
    """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_matrix_expression(p):
    """ expression : expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression
    """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_relational_expression(p):
    """ condition : expression EQ expression
                  | expression NEQ expression
                  | expression GEQ expression
                  | expression LEQ expression
                  | expression GT expression
                  | expression LT expression
    """
    p[0] = AST.Condition(p[2], p[1], p[3])


def p_negation_expression(p):
    """ expression : SUB expression %prec NEGATIVE """
    p[0] = AST.Negation(p[1], p[2])


def p_transposition_expression(p):
    """ expression : expression "'" """
    p[0] = AST.Transposition(p[2], p[1])


def p_functional_expression(p):
    """ expression : ZEROS '(' expression ')'
                   | ONES '(' expression ')'
                   | EYE '(' expression ')'
    """
    p[0] = AST.FunctionalExpression(p[1], p[3])


def p_matrix(p):
    """ expression : '[' vector_list ']'
                   | vector
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_vector_list(p):
    """ vector_list : vector_list ',' vector
                    | vector
    """
    if len(p) == 2:
        p[0] = AST.Matrix(p[1])
    else:
        p[0] = p[1]
        p[0].addVector(p[3])


def p_vector(p):
    """ vector : '[' number_list ']' """
    p[0] = p[2]


def p_number_list(p):
    """ number_list : number_list ',' variable
                    | number_list ',' INTNUM
                    | number_list ',' FLOAT
                    | variable
                    | INTNUM
                    | FLOAT
    """

    def _eval(x):
        return AST.IntNum(x) if isinstance(x, int) \
            else AST.FloatNum(x) if isinstance(x, float) else x

    if len(p) == 2:
        p[0] = AST.Vector(_eval(p[1]))
    else:
        p[0] = p[1]
        p[0].addNumber(_eval(p[3]))


def p_print(p):
    """ print : PRINT element_list ';' """
    p[0] = AST.Print(p[1], p[2])

def p_element_list(p):
    """ element_list : element_list ',' expression
                     | expression
    """
    if len(p) == 2:
        p[0] = AST.Elements(p[1])
    else:
        p[0] = p[1]
        p[0].addElement(p[3])





parser = yacc.yacc()
