from ..lab3 import AST  # noqa
from ..lab4 import SymbolTable  # noqa
from . import Memory    # noqa
from . import Exceptions    # noqa
from .visit import *    # pylint: disable=unused-wildcard-import
import sys
import numpy as np

sys.setrecursionlimit(10000)


arithmetic_ops = {
    '+': (lambda x, y: x + y),
    '+=': (lambda x, y: x + y),
    '-': (lambda x, y: x - y),
    '-=': (lambda x, y: x - y),
    '*': (lambda x, y: x * y if not isinstance(x, list) and not isinstance(y, list)
          else [z * y for z in x] if isinstance(x, list) and (x == [] or not isinstance(x[0], list))
          else [z * x for z in y] if isinstance(y, list) and (y == [] or not isinstance(y[0], list))
          else [[y * w for w in z] for z in x] if isinstance(x, list)
          else [[x * w for w in z] for z in y]),
    '*=': (lambda x, y: x * y),
    '/': (lambda x, y: x / y),
    '/=': (lambda x, y: x / y),
    '.+': (lambda x, y: ((np.matrix(x) + np.matrix(y)).tolist()[0])
           if not (isinstance(x, list) and isinstance(x[0], list)) and
           not (isinstance(y, list) and isinstance(y[0], list))
           else ((np.matrix(x) + np.matrix(y)).tolist())),
    '.-': (lambda x, y: ((np.matrix(x) - np.matrix(y)).tolist()[0])
           if not (isinstance(x, list) and isinstance(x[0], list)) and
           not (isinstance(y, list) and isinstance(y[0], list))
           else ((np.matrix(x) - np.matrix(y)).tolist())),
    '.*': (lambda x, y: np.multiply(np.array(x), np.array(y)).tolist()),
    './': (lambda x, y: np.divide(np.array(x), np.array(y)).tolist()),
}

relational_ops = {
    '==': (lambda x, y: x == y),
    '!=': (lambda x, y: x != y),
    '>': (lambda x, y: x > y),
    '<': (lambda x, y: x < y),
    '<=': (lambda x, y: x <= y),
    '>=': (lambda x, y: x >= y)
}


memory_stack = Memory.MemoryStack()

# flake8: noqa: F811
# pylama:ignore=W0404,W0401
# pylint: disable=function-redefined,no-member


class Interpreter():

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        try:
            node.instructions.accept(self)
        except Exceptions.BreakException:
            print('ups')
        except Exceptions.ContinueException:
            print('ups')

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Block)
    def visit(self, node):
        memory_stack.push(Memory.Memory('block'))
        node.instructions.accept(self)
        memory_stack.pop()

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return arithmetic_ops[node.op](r1, r2)

    @when(AST.Negation)
    def visit(self, node):
        value = node.expr.accept(self)
        if isinstance(value, list):
            return (- np.array(value)).tolist()  # pylint: disable=invalid-unary-operand-type
        return -value

    @when(AST.Transposition)
    def visit(self, node):
        return np.transpose(node.expr.accept(self)).tolist()

    @when(AST.FunctionalExpression)
    def visit(self, node):
        if node.func == 'eye':
            return getattr(np, node.func, lambda x: np.array([]))(*[x.accept(self)
                                                                    for x in node.dims.index_list]).tolist()
        return getattr(np, node.func, lambda x: np.array([]))([x.accept(self) for x in node.dims.index_list]).tolist()

    @when(AST.Assignment)
    def visit(self, node):
        value = node.expr.accept(self)
        if isinstance(node.var, AST.Ref):
            temp = np.array(memory_stack.get(node.var.name))
            index = tuple([x.accept(self) for x in node.var.index_list.index_list])
            temp[index] = value
            memory_stack.set_(node.var.name, temp.tolist())
        else:
            memory_stack.set_(node.var.name, value)

    @when(AST.ArithmeticAssignment)
    def visit(self, node):
        result = node.expr.accept(self)
        value = memory_stack.get(node.var.name)
        value = arithmetic_ops[node.op](value, result)
        memory_stack.set_(node.var.name, value)

    @when(AST.Condition)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return relational_ops[node.op](r1, r2)

    @when(AST.If)
    def visit(self, node):
        if node.cond.accept(self):
            node.if_instr.accept(self)
        elif node._else is not None:
            node.else_instr.accept(self)

    @when(AST.For)
    def visit(self, node):
        range_ = node.range_.accept(self)
        memory_stack.set_(node.var.name, range_[0])

        i = node.var.accept(self)
        while i < range_[1]:
            try:
                node.instr.accept(self)
            except Exceptions.BreakException:
                break
            except Exceptions.ContinueException:
                pass
            i = node.var.accept(self) + 1
            memory_stack.set_(node.var.name, i)

    @when(AST.Range)
    def visit(self, node):
        return (node.start.accept(self), node.stop.accept(self))

    @when(AST.Variable)
    def visit(self, node):
        return memory_stack.get(node.name)

    @when(AST.Elements)
    def visit(self, node):
        for elem in node.elems:
            yield elem.accept(self)

    @when(AST.Print)
    def visit(self, node):
        # print("PRINT: ", end='')
        for elem in node.elems.accept(self):
            print(elem, end=' ')
        print()

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Vector)
    def visit(self, node):
        return [number.accept(self) for number in node.number_list]

    @when(AST.Matrix)
    def visit(self, node):
        return [number.accept(self) for number in node.vector_list]

    @when(AST.Ref)
    def visit(self, node):
        value = np.array(memory_stack.get(node.name))
        index = tuple([x.accept(self) for x in node.index_list.index_list])
        return value[index].tolist() if isinstance(value[index], np.ndarray) else value[index]

    @when(AST.While)
    def visit(self, node):
        while node.cond.accept(self):
            try:
                node.instr.accept(self)
            except Exceptions.BreakException:
                break
            except Exceptions.ContinueException:
                pass

    @when(AST.Break)
    def visit(self, node):
        raise Exceptions.BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise Exceptions.ContinueException()
