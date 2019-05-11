from ..lab3 import AST  # noqa
from ..lab4 import SymbolTable  # noqa
from . import Memory    # noqa
from . import Exceptions    # noqa
from .visit import *    # noqa
import sys

sys.setrecursionlimit(10000)


arithmetic_ops = {
    '+': (lambda x, y: x + y),
    '+=': (lambda x, y: x + y),
    '-': (lambda x, y: x - y),
    '-=': (lambda x, y: x - y),
    '*': (lambda x, y: x * y),
    '*=': (lambda x, y: x * y),
    '/': (lambda x, y: x / y),
    '/=': (lambda x, y: x / y),
}

relational_ops = {
    '==': (lambda x, y: x == y),
    '!=': (lambda x, y: x != y),
    '>': (lambda x, y: x > y),
    '<': (lambda x, y: x < y),
    '<=': (lambda x, y: x <= y),
    '>=': (lambda x, y: x >= y)
}

assignment_ops = ['+=', '-=', '*=', '/=']


# flake8: noqa: F811
# pylama:ignore=W0404,W0401
# pylint: disable=function-redefined,no-member
class Interpreter():

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        pass
    #
    #

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
