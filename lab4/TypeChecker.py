from ..lab3 import AST  # noqa
from collections import defaultdict
from .SymbolTable import SymbolTable, VariableSymbol, MatrixSymbol


class ErrorBase:
    pass


class ErrorType(ErrorBase):
    def __str__(self):
        return 'ErrorType'


class ErrorSyntax(ErrorBase):
    def __str__(self):
        return 'ErrorSyntax'


class ErrorUndefined(ErrorBase):
    def __str__(self):
        return 'ErrorUndefined'


class ErrorOutOfBounds(ErrorBase):
    def __str__(self):
        return 'ErrorOutOfBounds'


class ErrorDimensions(ErrorBase):
    def __str__(self):
        return 'ErrorDimensions'


types = defaultdict(lambda: defaultdict(
    lambda: defaultdict(lambda: ErrorType())))

INTNUM = 'intnum'
FLOAT = 'float'
MATRIX = 'matrix'
VECTOR = 'vector'
STRING = 'string'
BOOLEAN = 'boolean'

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
    types[op][VECTOR][VECTOR] = VECTOR
    types[op][MATRIX][MATRIX] = MATRIX


for op in mul_div_ops:
    for dims in [MATRIX, VECTOR]:
        types[op][INTNUM][dims] = dims
        types[op][FLOAT][dims] = dims
        types[op][dims][INTNUM] = dims
        types[op][dims][FLOAT] = dims


for op in relational_ops:
    types[op][INTNUM][INTNUM] = BOOLEAN
    types[op][FLOAT][FLOAT] = BOOLEAN
    types[op][FLOAT][INTNUM] = BOOLEAN
    types[op][INTNUM][FLOAT] = BOOLEAN


types['=='][STRING][STRING] = BOOLEAN
types['!='][STRING][STRING] = BOOLEAN
# types['=='][MATRIX][MATRIX] = BOOLEAN
# types['!='][MATRIX][MATRIX] = BOOLEAN
# types['=='][VECTOR][VECTOR] = BOOLEAN
# types['!='][VECTOR][VECTOR] = BOOLEAN


types['-'][INTNUM] = INTNUM
types['-'][FLOAT] = FLOAT

types['zeros'][INTNUM] = MATRIX
types['eye'][INTNUM] = MATRIX
types['ones'][INTNUM] = MATRIX

types['+'][STRING][STRING] = STRING


class NodeVisitor():

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

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


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.nesting = 0

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)

        if isinstance(type1, ErrorBase):
            return type1

        if isinstance(type2, ErrorBase):
            return type2

        op = node.op
        type_ = types[op][type1][type2]

        if isinstance(type_, ErrorType):
            print(f'Type error at line {node.lineno}, column '
                  f'{node.colno}: {type1} {op} {type2}')

        return type_

    def visit_Negation(self, node):
        type_ = self.visit(node.expr)
        op = node.op
        if type_ not in (INTNUM, FLOAT):
            print(f'Type error at line {node.lineno}, column '
                  f'{node.colno}: {op} {type_}')
        return type_


    def visit_Ref(self, node):
        type__ = self.visit(node.index_list)
        if isinstance(type__, ErrorBase):
            return type__
        
        symbol = self.symbol_table.get(node.name)
        if not symbol:
            print(f'Undefined matrix at line {node.lineno}, column '
                   f'{node.colno}: {node.name}')
            return ErrorUndefined()

        type_ = symbol.type_
        dims = symbol.dims

        if type_ == MATRIX or type_ == VECTOR:          
            index_list = [index.value for index in node.index_list.index_list]

            if len(node.index_list.index_list) > len(dims):
                print(f'Dimensions out of bounds, line {node.lineno}, column '
                      f'{node.colno}: {type_} {node.name}, dimensions: {list(dims)}, index: {index_list}')
                return ErrorOutOfBounds()

            for index, dim in zip(node.index_list.index_list, dims):
                if index.value >= dim or index.value < 0:
                    print(f'Dimensions out of bounds, line {node.lineno}, column '
                          f'{node.colno}: {type_} {node.name}, dimensions: {list(dims)}, index: {index_list}')
                    return ErrorOutOfBounds()

            # if type_ == MATRIX:
            #     if len(index_list) == 2:
            #         type__ = self.visit(symbol.vector_list[index_list[0]].number_list[index_list[1]])
            #         print(type_)
            #         return type__
            return symbol.inner_type_
        else:
            print(f'Type error at line {node.lineno}, column '
                  f'{node.colno}: {type_} {node.index_list}')
            return ErrorType()


    def visit_IndexList(self, node):
        for index in node.index_list:
            type_ = self.visit(index)
            if type_ != INTNUM:
                print(f'Index error at line {node.lineno}, column 'f'{node.colno}: {type_}')
        return INTNUM
                

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_IntNum(self, node):
        return INTNUM

    def visit_FloatNum(self, node):
        return FLOAT

    def visit_String(self, node):
        return STRING

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            print(f'Undefined variable at line {node.lineno}, column '
                  f'{node.colno}: {node.name}')
            return ErrorUndefined()
        return symbol.type_

    def visit_Assignment(self, node):
        type_ = self.visit(node.expr)
        if not isinstance(type_, ErrorBase):
            if type_ == MATRIX and isinstance(node.expr, AST.Matrix):
                inner_type_ = self.visit(node.expr.vector_list[0].number_list[0])
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name,
                                                                  type_, inner_type_,
                                                                  (len(node.expr.vector_list),
                                                                          len(node.expr.vector_list[0].number_list),)))
            elif type_ == VECTOR and isinstance(node.expr, AST.Matrix):
                inner_type_ = self.visit(node.expr.number_list[0])
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name,
                                                                  type_, inner_type_, (len(node.expr.number_list),)))
            else:
                self.symbol_table.put(
                    node.var.name, VariableSymbol(node.var.name, type_))

    def visit_Matrix(self, node):
        number_of_vectors = len(node.vector_list) 
        vector_sizes = [len(vector.number_list) for vector in node.vector_list]

        if len(set(vector_sizes)) != 1:
            print(f'Matrix dimension error at line {node.lineno}, column '
                  f'{node.colno}: {number_of_vectors} x {vector_sizes}')
            return ErrorDimensions()

        for vector in node.vector_list:
            type_ = self.visit(vector)
            if isinstance(type_, ErrorBase):
                return type_

        return MATRIX

    def visit_Vector(self, node):
        types_ = set()
        for number in node.number_list:
            type_ = self.visit(number)
            types_.add(type_)
            if type_ not in (INTNUM, FLOAT):
                print(f'Matrix type error at line {node.lineno}, column '
                      f'{node.colno}: {type_}')
                return ErrorType()
        if len(types_) != 1:
            print(f'Mixed matrix type error at line {node.lineno}, column '
                  f'{node.colno}: {types_}')
            return ErrorType()
        return VECTOR

    def visit_ArithmeticAssignment(self, node):
        type1 = self.visit(node.var)
        type2 = self.visit(node.expr)

        if isinstance(type1, ErrorBase) or isinstance(type2, ErrorBase):
            return

        op = node.op
        type_ = types[op][type1][type2]

        if isinstance(type_, ErrorType):
            print(f'Type error at line {node.lineno}, column '
                  f'{node.colno}: {type1} {op} {type2}')
        else:
            self.symbol_table.put(
                node.var.name, VariableSymbol(node.var, type_))

    def visit_Error(self, node):
        return ErrorSyntax()
