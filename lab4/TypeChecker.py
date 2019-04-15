from ..lab3 import AST  # noqa
from collections import defaultdict
from . import SymbolTable, VariableTable


def nesteddict():
    return defaultdict(nesteddict)


types = nesteddict()
# symbols = SymbolTable.SymbolTable()

INTNUM = 'intnum'
FLOAT = 'float'
MATRIX = 'matrix'

mul_div_ops = ['*', '/']
arithmetic_ops = mul_div_ops + ['+', '-']
matrix_ops = ['.+', '.-', '.*', './']
relational_ops = ['<', '>', '>=', '<=', '==', '!=']
assignment_ops = ['+=', '-=', '*=', '/=']


for op in arithmetic_ops + assignment_ops:
    types[op][INTNUM][INTNUM] = INTNUM
    types[op][INTNUM][FLOAT] = FLOAT
    types[op][FLOAT][INTNUM] = FLOAT
    types[op][FLOAT][FLOAT] = FLOAT


for op in matrix_ops:
    types[op][MATRIX][MATRIX] = MATRIX


for op in mul_div_ops:
    types[op][INTNUM][MATRIX] = MATRIX
    types[op][FLOAT][MATRIX] = MATRIX
    types[op][MATRIX][INTNUM] = MATRIX
    types[op][MATRIX][FLOAT] = MATRIX


class ErrorType:

    def __str__(self):
        return 'ErrorType'


class NodeVisitor():

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # Called if no explicit visitor function exists for a node.
    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.nesting = 0

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op



    def visit_Ref(self, node):
        pass

    def visit_Program(self, node):
        self.visit(node.instructions)
    
    def visit_Instructions(self, node):
        type_ = None
        for instruction in node.instructions:
            type_ = self.visit(instruction)
            if isinstance(type_, ErrorType):
                break
        return type_
    
    def visit_Instruction(self, node):
        return self.visit(node.instruction)


    def visit_IntNum(self, node):
        return INTNUM


    def visit_Variable(self, node):
        return 



    