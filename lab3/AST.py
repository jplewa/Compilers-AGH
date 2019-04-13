RANGE = 'RANGE'
REF = 'REF'
THEN = 'THEN'
VECTOR = 'VECTOR'
TRANSPOSE = 'TRANSPOSE'


class Node():
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class IndexList(Node):
    def __init__(self, index):
        self.index_list = [index]

    def addIndex(self, index):
        self.index_list.append(index)


class Vector(Node):
    def __init__(self, number):
        self.keyword = VECTOR
        self.number_list = [number]

    def addNumber(self, number):
        self.number_list.append(number)


class Matrix(Node):
    def __init__(self, vector):
        self.keyword = VECTOR
        self.vector_list = [vector]

    def addVector(self, vector):
        self.vector_list.append(vector)


class Ref(Node):
    def __init__(self, name, index_list):
        self.keyword = REF
        self.name = name
        self.index_list = index_list


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Condition(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class FunctionalExpression(Node):
    def __init__(self, func, expr):
        self.func = func
        self.expr = expr


class Transposition(Node):
    def __init__(self, _, expr):
        self.keyword = TRANSPOSE
        self.expr = expr


class Negation(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instruction):
        self.instructions = [instruction]

    def addInstruction(self, instruction):
        self.instructions.append(instruction)


class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction


class Block(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class If(Node):
    def __init__(self, _if, cond, if_instr, _else=None, else_instr=None):
        self._if = str.upper(_if)
        self.cond = cond
        self._then = THEN
        self.if_instr = if_instr
        self._else = str.upper(_else) if _else else _else
        self.else_instr = else_instr


class For(Node):
    def __init__(self, _for, var, _range, instr):
        self._for = str.upper(_for)
        self.var = var
        self._range = _range
        self.instr = instr


class Range(Node):
    def __init__(self, _, start, stop):
        self.keyword = RANGE
        self.start = start
        self.stop = stop


class While(Node):
    def __init__(self, _while, cond, expr):
        self._while = str.upper(_while)
        self.cond = cond
        self.expr = expr


class Elements(Node):
    def __init__(self, elem):
        self.elems = [elem]

    def addElement(self, elem):
        self.elems.append(elem)


class Assignment(Node):
    def __init__(self, op, var, expr):
        self.var = var
        self.op = op
        self.expr = expr


class ArithmeticAssignment(Node):
    def __init__(self, op, var, expr):
        self.var = var
        self.op = op
        self.expr = expr


class Return(Node):
    def __init__(self, keyword, expr):
        self.keyword = str.upper(keyword)
        self.expr = expr


class Print(Node):
    def __init__(self, keyword, elems):
        self.keyword = str.upper(keyword)
        self.elems = elems


class Break(Node):
    def __init__(self, keyword):
        self.keyword = str.upper(keyword)


class Continue(Node):
    def __init__(self, keyword):
        self.keyword = str.upper(keyword)


class Error(Node):
    def __init__(self):
        pass
