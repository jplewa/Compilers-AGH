from __future__ import print_function
from . import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


# flake8: noqa: F811
# pylama:ignore=W0404
# pylint: disable=function-redefined,no-member
class TreePrinter:

    @addToClass(AST.Node)
    def printWithIndent(self, xd, indent=0):
        print(f'{"|  " * indent}{xd}')

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception(f'printTree not defined in class \
            {self.__class__.__name__}')

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        self.printWithIndent(self.value, indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        self.printWithIndent(self.value, indent)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        self.printWithIndent(self.value, indent)

    # @addToClass(AST.Error)
    # def printTree(self, indent=0):
    #     pass
    #     # fill in the body

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        self.printWithIndent(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        self.printWithIndent(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        self.printWithIndent(self._if, indent)
        self.cond.printTree(indent + 1)
        self.printWithIndent(self._then, indent)
        self.if_instr.printTree(indent + 1)
        if self._else and self.else_instr:
            self.printWithIndent(self._else, indent)
            self.else_instr.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        self.printWithIndent(self._for, indent)
        self.var.printTree(indent + 1)
        self._range.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        self.start.printTree(indent + 1)
        self.stop.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        self.printWithIndent(self._while, indent)
        self.cond.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.FunctionalExpression)
    def printTree(self, indent=0):
        self.printWithIndent(self.func, indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Negation)
    def printTree(self, indent=0):
        self.printWithIndent(self.op, indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        if self.instructions:
            for instruction in self.instructions:
                instruction.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        self.printWithIndent(self.op, indent)
        self.var.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.ArithmeticAssignment)
    def printTree(self, indent=0):
        self.printWithIndent(self.op, indent)
        self.var.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        for elem in self.elems.elems:
            elem.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        self.printWithIndent(self.name, indent)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        self.printWithIndent(self.name, indent + 1)
        self.index_list.printTree(indent + 1)

    @addToClass(AST.IndexList)
    def printTree(self, indent=0):
        for index in self.index_list:
            index.printTree(indent)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        for vector in self.vector_list:
            vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        self.printWithIndent(self.keyword, indent)
        for number in self.number_list:
            number.printTree(indent + 1)
