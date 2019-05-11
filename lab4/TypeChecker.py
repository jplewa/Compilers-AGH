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

types[':'][INTNUM][INTNUM] = INTNUM

# types['=='][STRING][STRING] = BOOLEAN
# types['!='][STRING][STRING] = BOOLEAN
# types['=='][MATRIX][MATRIX] = BOOLEAN
# types['!='][MATRIX][MATRIX] = BOOLEAN
# types['=='][VECTOR][VECTOR] = BOOLEAN
# types['!='][VECTOR][VECTOR] = BOOLEAN


# types['-'][INTNUM] = INTNUM
# types['-'][FLOAT] = FLOAT

# types['+'][STRING][STRING] = STRING


class NodeVisitor():

    def visit(self, node, name=None):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if name is None:
            return visitor(node)
        else:
            return visitor(node, name)

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

            if type_ == MATRIX:
                if len(index_list) == 1:
                    return VECTOR
                if len(index_list) == 2:
                    type__ = symbol.inner_type_
                    return type__
            return symbol.inner_type_
        else:
            print(f'Type error at line {node.lineno}, column '
                  f'{node.colno}: {type_} {[x.value for x in node.index_list.index_list]}')
            return ErrorType()


    def visit_IndexList(self, node):
        for index in node.index_list:
            type_ = self.visit(index)
            if type_ != INTNUM:
                print(f'Index error at line {node.lineno}, column 'f'{node.colno}: {type_}')
                return type_
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
            if isinstance(expr, AST.Variable):
                type_ = self.visit(expr)
                if type_ in [VECTOR, MATRIX]:
                    inner_type_ = self.symbol_table.get(expr.name).inner_type_
                    dims = self.symbol_table.get(expr.name).dims                       
                else:
                    inner_type_ = type_
                    dims = None
            elif isinstance(expr, AST.Vector):
                type_ = self.visit(expr)
                if not isinstance(type_, ErrorBase):
                    inner_type_ = self.visit(expr.number_list[0])
                    dims = (len(expr.number_list),)
            elif isinstance(expr, AST.Matrix):
                type_ = self.visit(expr)
                if not isinstance(type_, ErrorBase):
                    inner_type_ = self.visit(expr.vector_list[0].number_list[0])
                    dims = (len(expr.vector_list), len(expr.vector_list[0].number_list),)
            elif isinstance(expr, AST.Transposition):
                type_ = self.visit(expr)
                if not isinstance(type_, ErrorBase):
                    inner_type_ = self.visit(expr.vector_list[0].number_list[0])
                    dims = (len(expr.vector_list[0].number_list), len(expr.vector_list),)
            else:
                type_ = self.visit(expr)
                inner_type_ = type_
                dims = None
            all_dims += [dims]
            all_inner_types += [inner_type_]         
        result_dim = None
        all_dims = set([dim for dim in all_dims if dim is not None])
        if len(all_dims) > 1:
            print(f'Matrix dimension error at line {node.lineno}, column '
                  f'{node.colno}: {all_dims}')
            result_dim = ErrorDimensions()
        elif len(all_dims) == 1:
            result_dim = list(all_dims)[0]
        else:
            result_dim = None

        return (INTNUM if all([b == INTNUM for b in all_inner_types]) else FLOAT), result_dim

    def visit_Assignment(self, node):
        type_ = self.visit(node.expr)
        if not isinstance(type_, ErrorBase):
            if type_ == VECTOR and isinstance(node.expr, AST.Ref):
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
                xd = node.expr.expr
                if isinstance(xd, AST.Variable):
                    lol = self.symbol_table.get(xd.name)
                    lol.name = node.var.name
                    lol.dims = tuple(reversed(lol.dims))
                    self.symbol_table.put(node.var.name, lol)
                else:
                    inner_type_ = self.visit(node.expr.vector_list[0].number_list[0])
                    dims = (len(node.expr.vector_list[0].number_list), len(node.expr.vector_list),)
                    self.symbol_table.put(node.var.name, MatrixSymbol(node.var.name, type_, inner_type_, dims))
            else:
                self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_))

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
            print(f'Mixed inner matrix types at line {node.lineno}, column '
                  f'{node.colno}: {inner_types_}')
            return ErrorType()

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

    def visit_FunctionalExpression(self, node):
        type_ = self.visit(node.dims)
        if isinstance(type_, ErrorBase):
            return type_
        
        if len (node.dims.index_list) > 2:
            print(f'Too many arguments at {node.lineno}, column '
                  f'{node.colno}: function {node.func}, expected 1D or 2D')
            return ErrorDimensions()
        
        if len(node.dims.index_list) == 2:
            return MATRIX
        if len(node.dims.index_list) == 1:
            return VECTOR

    def visit_Continue(self, node):
        name = self.symbol_table.name
        parent = self.symbol_table.parent

        if name not in ['while', 'for']:
            while parent is not None:
                if parent.name in  ['while', 'for']:
                    name = parent.name
                    break
                parent = parent.parent
                
        if name not in ['while', 'for']:
            print(f'Continue instruction outside of loop at line {node.lineno}, column '
                  f'{node.colno}')

    def visit_Break(self, node):
        name = self.symbol_table.name
        parent = self.symbol_table.parent

        if name not in ['while', 'for']:
            while parent is not None:
                if parent.name in  ['while', 'for']:
                    name = parent.name
                    break
                parent = parent.parent
                
        if name not in ['while', 'for']:
            print(f'Break instruction outside of loop at line {node.lineno}, column '
                  f'{node.colno}')
            
    def visit_Block(self, node, name='block'):
        self.symbol_table = self.symbol_table.pushScope(name)
        for instruction in node.instructions.instructions:
            self.visit(instruction)
        self.symbol_table.prettyPrint()
        self.symbol_table = self.symbol_table.popScope()

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

    def visit_If(self, node):
        self.visit(node.cond)

        if not isinstance(node.if_instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('if')
            self.visit(node.if_instr, None)
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            self.visit(node.if_instr, 'if')
            
        if node.else_instr is not None:
            if not isinstance(node.else_instr, AST.Block):
                self.symbol_table = self.symbol_table.pushScope('else')
                self.visit(node.else_instr, None)
                self.symbol_table.prettyPrint()
                self.symbol_table = self.symbol_table.popScope()
            else:
                self.visit(node.else_instr, 'else')

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
            print(f'Type error in range at line {node.lineno}, column '
                  f'{node.colno}: {start_type} : {stop_type}') 
        return type_

    def visit_For(self, node):
        type_ = self.visit(node.range_)
        if not isinstance(type_, ErrorType):
            self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_))
        if not isinstance(node.instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('for')
            self.visit(node.instr, None)
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            self.visit(node.instr, 'for')
    
    def visit_Transposition(self,node):
        type_ = self.visit(node.expr)
        if type_ != MATRIX:
            print(f'Type error in transposition at line {node.lineno}, column '
                  f'{node.colno}: {type_}')
            type_ = ErrorType()
        return type_
        
    def visit_Return(self, node):
        type_ = self.visit(node.expr)
        if not isinstance(type_, ErrorBase):
            if isinstance(node.expr, AST.BinExpr):
                self.eval_BinExpr(node.expr)

    def visit_While(self, node):
        self.visit(node.cond)

        if not isinstance(node.instr, AST.Block):
            self.symbol_table = self.symbol_table.pushScope('while')
            self.visit(node.instr, None)
            self.symbol_table.prettyPrint()
            self.symbol_table = self.symbol_table.popScope()
        else:
            self.visit(node.instr, 'while')

    def visit_Print(self, node):
        self.visit(node.elems)

    def visit_Elements(self, node):
        for elem in node.elems:
            if isinstance(elem, AST.BinExpr):
                self.eval_BinExpr(elem)
            self.visit(elem)

    def visit_Error(self, _):
        return ErrorSyntax()
