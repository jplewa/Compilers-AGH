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


types = defaultdict(lambda: defaultdict(lambda: defaultdict(ErrorType)))

LOOP_TYPES = ['while', 'for']

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


for dims in [MATRIX, VECTOR]:
    types['*'][INTNUM][dims] = dims
    types['*'][FLOAT][dims] = dims
    types['*'][dims][INTNUM] = dims
    types['*'][dims][FLOAT] = dims


for op in relational_ops:
    types[op][INTNUM][INTNUM] = BOOLEAN
    types[op][FLOAT][FLOAT] = BOOLEAN
    types[op][FLOAT][INTNUM] = BOOLEAN
    types[op][INTNUM][FLOAT] = BOOLEAN

types[':'][INTNUM][INTNUM] = INTNUM


class NodeVisitor():

    def visit(self, node, name=None):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node) if name is None else visitor(node, name)

    def generic_visit(self, node):

        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif node is not None:
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

    def visit_Program(self, node):
        return self.visit(node.instructions)

    def visit_Instructions(self, node):
        error = None
        for instruction in node.instructions:
            type_ = self.visit(instruction)
            if isinstance(type_, ErrorBase):
                error = type_
        return error

    def visit_Block(self, node, name='block'):
        error = None
        self.symbol_table = self.symbol_table.pushScope(name)
        for instruction in node.instructions.instructions:
            type_ = self.visit(instruction)
            if isinstance(type_, ErrorBase):
                error = type_
        self.symbol_table.prettyPrint()
        self.symbol_table = self.symbol_table.popScope()
        return error

    def visit_Assignment(self, node):
        type_ = self.visit(node.expr)
        if not isinstance(type_, ErrorBase):
            if isinstance(node.var, AST.Ref):
                var_type = self.visit(node.var)
                if not isinstance(var_type, ErrorBase):
                    if var_type != type_:
                        print(f'Type error at line {node.lineno}, column {node.colno}: {var_type} = {type_}')
                        type_ = ErrorType()
                    elif type_ == VECTOR and var_type == VECTOR and isinstance(node.expr, AST.Vector):
                        inner_type_ = self.symbol_table.get(node.var.name).inner_type_
                        dims = (self.symbol_table.get(node.var.name).dims[1],)
                        inner_type_r = self.visit(node.expr.number_list[0])
                        dims_r = (len(node.expr.number_list),)
                        if inner_type_ != inner_type_r:
                            print(f'Type error at line {node.lineno}, column {node.colno}: {var_type}[{inner_type_}] = {type_}[{inner_type_r}]')
                            type_ = ErrorDimensions()
                        elif dims_r[0] >= dims[0]:
                            print(f'Dimension error at line {node.lineno}, column {node.colno}')
                            type_ = ErrorDimensions()
                else:
                    type_ = var_type
            elif type_ == VECTOR and isinstance(node.expr, AST.Ref):
                inner_type_ = self.symbol_table.get(node.expr.name).inner_type_
                dims = (self.symbol_table.get(node.expr.name).dims[1],)
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            elif type_ == MATRIX and isinstance(node.expr, AST.Matrix):
                inner_type_ = self.visit(node.expr.vector_list[0].number_list[0])
                dims = (len(node.expr.vector_list), len(node.expr.vector_list[0].number_list),)
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            elif type_ == VECTOR and isinstance(node.expr, AST.Vector):
                inner_type_ = self.visit(node.expr.number_list[0])
                dims = (len(node.expr.number_list),)
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            elif (type_ in [VECTOR, MATRIX]) and isinstance(node.expr, AST.BinExpr):
                inner_type_, dims = self.eval_BinExpr(node.expr)
                if not isinstance(dims, ErrorBase):
                    self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            elif (type_ in [VECTOR, MATRIX]) and isinstance(node.expr, AST.FunctionalExpression):
                dims = tuple([x.value for x in node.expr.dims.index_list])
                self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, INTNUM, dims))
            elif type_ == MATRIX and isinstance(node.expr, AST.Transposition):
                expr = node.expr.expr
                if isinstance(expr, AST.Variable):
                    variable = self.symbol_table.get(expr.name)
                    variable.name = node.var.name
                    variable.dims = tuple(reversed(variable.dims))
                    self.symbol_table.put(node.var.name, variable)
                else:
                    inner_type_ = self.visit(node.expr.vector_list[0].number_list[0])
                    dims = (len(node.expr.vector_list[0].number_list), len(node.expr.vector_list),)
                    self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            else:
                self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_))
        return type_ if isinstance(type_, ErrorBase) else None

    def visit_ArithmeticAssignment(self, node):
        type1 = self.visit(node.var)
        type2 = self.visit(node.expr)

        if isinstance(type1, ErrorBase):
            return type1
        
        if isinstance(type2, ErrorBase):
            return type2

        op = node.op
        type_ = types[op][type1][type2]

        if isinstance(type_, ErrorType):
            print(f'Type error at line {node.lineno}, column {node.colno}: {type1} {op} {type2}')
        else:
            self.symbol_table.put(node.var.name, VariableSymbol(node.var, type_))
        
        return type_ if isinstance(type_, ErrorBase) else None
        
    def visit_If(self, node):
        type_ = self.visit(node.cond)
        error = type_ if isinstance(type_, ErrorBase) else None

        if not isinstance(node.if_instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('if')
            instr_type = self.visit(node.if_instr, None)
            error = instr_type if isinstance(type_, ErrorBase) else error
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            instr_type = self.visit(node.if_instr, 'if')
            error = instr_type if isinstance(type_, ErrorBase) else error

        if node.else_instr is not None:
            if not isinstance(node.else_instr, AST.Block):
                self.symbol_table = self.symbol_table.pushScope('else')
                instr_type = self.visit(node.else_instr, None)
                error = instr_type if isinstance(type_, ErrorBase) else error
                self.symbol_table.prettyPrint()
                self.symbol_table = self.symbol_table.popScope()
            else:
                instr_type = self.visit(node.else_instr, 'else')
                error = instr_type if isinstance(type_, ErrorBase) else error

        return error

    def visit_While(self, node):
        type_ = self.visit(node.cond)
        error = type_ if isinstance(type_, ErrorBase) else None

        if not isinstance(node.instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('while')
            instr_type = self.visit(node.instr, None)
            error = instr_type if isinstance(type_, ErrorBase) else error
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            instr_type = self.visit(node.instr, 'while')
            error = instr_type if isinstance(type_, ErrorBase) else error

        return error

    def visit_For(self, node):
        type_ = self.visit(node.range_)
        error = type_ if isinstance(type_, ErrorBase) else None

        if not isinstance(type_, ErrorType):
            self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_))
        if not isinstance(node.instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('for')
            instr_type = self.visit(node.instr, None)
            error = instr_type if isinstance(type_, ErrorBase) else error
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            instr_type = self.visit(node.instr, 'for')
            error = instr_type if isinstance(type_, ErrorBase) else error

        return error

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        stop_type = self.visit(node.stop)

        if isinstance(node.start, AST.BinExpr):
            type_, dims = self.eval_BinExpr(node.start)
            if isinstance(dims, ErrorBase):
                return type_

        if isinstance(node.stop, AST.BinExpr):
            type_, dims = self.eval_BinExpr(node.stop)
            if isinstance(dims, ErrorBase):
                return type_

        type_ = types[':'][start_type][stop_type]
        if isinstance(type_, ErrorType):
            print(f'Type error in range at line {node.lineno}, column {node.colno}: {start_type} : {stop_type}')
        return type_

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            print(f'Undefined variable at line {node.lineno}, column {node.colno}: {node.name}')
            return ErrorUndefined()
        return symbol.type_

    def visit_Ref(self, node):
        type__ = self.visit(node.index_list)
        if isinstance(type__, ErrorBase):
            return type__

        symbol = self.symbol_table.get(node.name)
        if not symbol:
            print(f'Undefined matrix at line {node.lineno}, column {node.colno}: {node.name}')
            return ErrorUndefined()

        type_ = symbol.type_
        dims = symbol.dims

        if type_ in [MATRIX, VECTOR]:
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

            if type_ == MATRIX:
                if len(index_list) == 1:
                    return VECTOR
                if len(index_list) == 2:
                    type__ = symbol.inner_type_
                    return type__

            return symbol.inner_type_

        print(f'Type error at line {node.lineno}, column '
              f'{node.colno}: {type_} {[x.value for x in node.index_list.index_list]}')
        return ErrorType()

    def visit_IndexList(self, node):
        for index in node.index_list:
            type_ = self.visit(index)
            if type_ != INTNUM:
                print(f'Index error at line {node.lineno}, column {node.colno}: {type_}')
                return type_
        return INTNUM

    def visit_Return(self, node):
        dims = None
        type_ = self.visit(node.expr)
        if not isinstance(type_, ErrorBase):
            if isinstance(node.expr, AST.BinExpr):
                _, dims = self.eval_BinExpr(node.expr)
            return dims
        return type_

    def visit_Break(self, node):
        name = self.symbol_table.name
        parent = self.symbol_table.parent

        if name not in LOOP_TYPES:
            while parent is not None:
                if parent.name in LOOP_TYPES:
                    name = parent.name
                    break
                parent = parent.parent

        if name not in LOOP_TYPES:
            print(f'Break instruction outside of loop at line {node.lineno}, column {node.colno}')
            return ErrorBase()

        return None

    def visit_Continue(self, node):
        name = self.symbol_table.name
        parent = self.symbol_table.parent

        if name not in LOOP_TYPES:
            while parent is not None:
                if parent.name in LOOP_TYPES:
                    name = parent.name
                    break
                parent = parent.parent

        if name not in LOOP_TYPES:
            print(f'Continue instruction outside of loop at line {node.lineno}, column {node.colno}')
            return ErrorBase()
        
        return None

    def visit_IntNum(self, _):
        return INTNUM

    def visit_FloatNum(self, _):
        return FLOAT

    def visit_String(self, _):
        return STRING

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
            print(f'Type error at line {node.lineno}, column {node.colno}: {type1} {op} {type2}')

        return type_

    def visit_Condition(self, node):
        if isinstance(node.left, AST.BinExpr):
            if isinstance(self.eval_BinExpr(node.left)[1], ErrorBase):
                return ErrorBase()
        if isinstance(node.right, AST.BinExpr):
            if isinstance(self.eval_BinExpr(node.right)[1], ErrorBase):
                return ErrorBase()

        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if isinstance(type_left, ErrorBase):
            return type_left

        if isinstance(type_right, ErrorBase):
            return type_right

        type_ = types[node.op][type_left][type_right]

        if isinstance(type_, ErrorBase):
            print(f'Type error at line {node.lineno}, column {node.colno}: {type_left} {node.op} {type_right}')
        return type_

    def visit_Negation(self, node):
        type_ = self.visit(node.expr)
        op = node.op
        if type_ not in (INTNUM, FLOAT):
            print(f'Type error at line {node.lineno}, column {node.colno}: {op} {type_}')
        return type_

    def visit_Transposition(self, node):
        type_ = self.visit(node.expr)
        if type_ != MATRIX:
            print(f'Type error in transposition at line {node.lineno}, column {node.colno}: {type_}')
            type_ = ErrorType()
        return type_

    def visit_FunctionalExpression(self, node):
        type_ = self.visit(node.dims)
        if not isinstance(type_, ErrorBase):
            if len(node.dims.index_list) > 2:
                print(f'Too many arguments at {node.lineno}, column '
                      f'{node.colno}: function {node.func}, expected 1D or 2D')
                type_ = ErrorDimensions()
            elif len(node.dims.index_list) == 2:
                type_ = MATRIX
            if len(node.dims.index_list) == 1:
                type_ = VECTOR
        return type_

    def visit_Matrix(self, node):
        number_of_vectors = len(node.vector_list)
        vector_sizes = [len(vector.number_list) for vector in node.vector_list]

        if len(set(vector_sizes)) != 1:
            print(f'Matrix dimension error at line {node.lineno}, column '
                  f'{node.colno}: {number_of_vectors} x {vector_sizes}')
            return ErrorDimensions()

        inner_types_ = []
        for vector in node.vector_list:
            type_ = self.visit(vector)
            inner_types_ += [self.visit(vector.number_list[0])]
            if isinstance(type_, ErrorBase):
                return type_
        if len(set(inner_types_)) != 1:
            print(f'Mixed inner matrix types at line {node.lineno}, column {node.colno}: {inner_types_}')
            return ErrorType()

        return MATRIX

    def visit_Vector(self, node):
        types_ = set()
        for number in node.number_list:
            type_ = self.visit(number)
            types_.add(type_)
            if type_ not in (INTNUM, FLOAT):
                print(f'Matrix type error at line {node.lineno}, column {node.colno}: {type_}')
                return ErrorType()
        if len(types_) != 1:
            print(f'Mixed matrix type error at line {node.lineno}, column {node.colno}: {types_}')
            return ErrorType()
        return VECTOR

    def visit_Print(self, node):
        return self.visit(node.elems)

    def visit_Elements(self, node):
        error = None
        for elem in node.elems:
            if isinstance(elem, AST.BinExpr):
                _, dims = self.eval_BinExpr(elem)
                error = dims if isinstance(dims, ErrorBase) else error
            
            type_ = self.visit(elem)
            error = type_ if isinstance(type_, ErrorBase) else error
        
        return error

    def eval_BinExpr(self, node):
        tail = [node.right]
        head = node.left
        while isinstance(head, AST.BinExpr):
            tail.append(head.right)
            head = head.left
        tail.append(head)
        all_dims = []
        all_inner_types = []
        for expr in tail:
            type_ = self.visit(expr)
            inner_type_, dims = type_, None
            if not isinstance(type_, ErrorBase):
                if isinstance(expr, AST.Variable):
                    if type_ in [VECTOR, MATRIX]:
                        inner_type_ = self.symbol_table.get(expr.name).inner_type_
                        dims = self.symbol_table.get(expr.name).dims
                    else:
                        inner_type_, dims = type_, None
                elif isinstance(expr, AST.Vector):
                    inner_type_ = self.visit(expr.number_list[0])
                    dims = (len(expr.number_list),)
                elif isinstance(expr, AST.Matrix):
                    inner_type_ = self.visit(expr.vector_list[0].number_list[0])
                    dims = (len(expr.vector_list), len(expr.vector_list[0].number_list),)
                elif isinstance(expr, AST.Transposition):
                    if isinstance(expr.expr, AST.Matrix):
                        inner_type_ = self.visit(expr.vector_list[0].number_list[0])
                        dims = (len(expr.vector_list[0].number_list), len(expr.vector_list),)
                    elif isinstance(expr.expr, AST.Variable):
                        inner_type_ = self.symbol_table.get(expr.expr.name).inner_type_
                        dims = self.symbol_table.get(expr.expr.name).dims
                        dims = tuple(reversed(dims))
            all_dims += [dims]
            all_inner_types += [inner_type_]
        result_dim = None
        all_dims = {dim for dim in all_dims if dim is not None}
        if len(all_dims) > 1:
            print(f'Matrix dimension error at line {node.lineno}, column {node.colno}: {all_dims}')
            result_dim = ErrorDimensions()
        else:
            result_dim = list(all_dims)[0] if len(all_dims) == 1 else None
        return (INTNUM if all([b == INTNUM for b in all_inner_types]) else FLOAT), result_dim

    def visit_Error(self, _):
        return ErrorSyntax()
