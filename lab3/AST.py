RANGE = 'RANGE'
REF = 'REF'
THEN = 'THEN'
VECTOR = 'VECTOR'
TRANSPOSE = 'TRANSPOSE'


class Node():
    pass


class Program(Node):
    def __init__(self, instructions=None, lineno=1, colno=1):
        self.instructions = instructions
        self.lineno = lineno
        self.colno = colno


class Instructions(Node):
    def __init__(self, instruction, lineno, colno):
        self.instructions = [instruction]
        self.lineno = lineno
        self.colno = colno

    def addInstruction(self, instruction):
        self.instructions.append(instruction)


class Block(Node):
    def __init__(self, instructions, lineno, colno):
        self.instructions = instructions
        self.lineno = lineno
        self.colno = colno


class Assignment(Node):
    def __init__(self, op, var, expr, lineno, colno):   # noqa
        self.var = var
        self.op = op
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class ArithmeticAssignment(Node):
    def __init__(self, op, var, expr, lineno, colno):   # noqa
        self.var = var
        self.op = op
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class If(Node):
    def __init__(self, _if, cond, if_instr, lineno, colno, _else=None, else_instr=None):    # noqa
        self._if = str.upper(_if)
        self.cond = cond
        self._then = THEN
        self.if_instr = if_instr
        self.lineno = lineno
        self.colno = colno
        self._else = str.upper(_else) if _else else _else
        self.else_instr = else_instr


class While(Node):
    def __init__(self, _while, cond, expr, lineno, colno):
        self._while = str.upper(_while)
        self.cond = cond
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class For(Node):
    def __init__(self, _for, var, _range, instr, lineno, colno):
        self._for = str.upper(_for)
        self.var = var
        self._range = _range
        self.instr = instr
        self.lineno = lineno
        self.colno = colno


class Range(Node):
    def __init__(self, _, start, stop, lineno, colno):
        self.keyword = RANGE
        self.start = start
        self.stop = stop
        self.lineno = lineno
        self.colno = colno


class Variable(Node):
    def __init__(self, name, lineno, colno):
        self.name = name
        self.lineno = lineno
        self.colno = colno


class Ref(Node):
    def __init__(self, name, index_list, lineno, colno):
        self.keyword = REF
        self.name = name
        self.index_list = index_list
        self.lineno = lineno
        self.colno = colno


class IndexList(Node):
    def __init__(self, index, lineno, colno):
        self.index_list = [index]
        self.lineno = lineno
        self.colno = colno

    def addIndex(self, index):
        self.index_list.append(index)


class Return(Node):
    def __init__(self, keyword, expr, lineno, colno):
        self.keyword = str.upper(keyword)
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class Break(Node):
    def __init__(self, keyword, lineno, colno):
        self.keyword = str.upper(keyword)
        self.lineno = lineno
        self.colno = colno


class Continue(Node):
    def __init__(self, keyword, lineno, colno):
        self.keyword = str.upper(keyword)
        self.lineno = lineno
        self.colno = colno


class IntNum(Node):
    def __init__(self, value, lineno, colno):
        self.value = value
        self.lineno = lineno
        self.colno = colno


class FloatNum(Node):
    def __init__(self, value, lineno, colno):
        self.value = value
        self.lineno = lineno
        self.colno = colno


class String(Node):
    def __init__(self, value, lineno, colno):
        self.value = value
        self.lineno = lineno
        self.colno = colno


class BinExpr(Node):
    def __init__(self, op, left, right, lineno, colno): # noqa
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
        self.colno = colno


class Condition(Node):
    def __init__(self, op, left, right, lineno, colno): # noqa
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
        self.colno = colno


class Negation(Node):
    def __init__(self, op, expr, lineno, colno):
        self.op = op
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class Transposition(Node):
    def __init__(self, expr, lineno, colno):
        self.keyword = TRANSPOSE
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class FunctionalExpression(Node):
    def __init__(self, func, expr, lineno, colno):
        self.func = func
        self.expr = expr
        self.lineno = lineno
        self.colno = colno


class Matrix(Node):
    def __init__(self, lineno, colno):
        self.keyword = VECTOR
        self.vector_list = []
        self.lineno = lineno
        self.colno = colno

    def addVector(self, vector):
        self.vector_list.append(vector)
 

class Vector(Node):
    def __init__(self, number, lineno, colno):
        self.keyword = VECTOR
        self.number_list = [number]
        self.lineno = lineno
        self.colno = colno

    def addNumber(self, number):
        self.number_list.append(number)


class Print(Node):
    def __init__(self, keyword, elems, lineno, colno):
        self.keyword = str.upper(keyword)
        self.elems = elems
        self.lineno = lineno
        self.colno = colno


class Elements(Node):
    def __init__(self, elem, lineno, colno):
        self.elems = [elem]
        self.lineno = lineno
        self.colno = colno

    def addElement(self, elem):
        self.elems.append(elem)


class Error(Node):
    def __init__(self, value, lineno, colno):
        self.value = value
        self.lineno = lineno
        self.colno = colno
