class Symbol:   # class to inherit below
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __str__(self):
        return str(self.type_)


class MatrixSymbol(Symbol):
    def __init__(self, name, type_, inner_type_, dims):
        self.name = name
        self.type_ = type_
        self.inner_type_ = inner_type_
        self.dims = dims

    def __str__(self):
        return str(self.type_)


class SymbolTable():

    def __init__(self, parent, name):   # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.variables = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.variables[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        # print(">>>>>", self.variables)
        symbol = self.variables.get(name, None)
        if symbol is None and self.parent is not None:
            symbol = self.getParentScope().get(name)
        return symbol

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent

    def __str__(self):
        result = f'-----{self.name} P:{self.parent.name if self.parent else "None"}-----\n'
        result += {key: value.__str__() for key, value in self.variables.items()}.__str__()
        return result

    def prettyPrint(self):
        print('================')
        parent = self.getParentScope()
        result = ''

        parents = []

        while parent is not None:
            parents.append(parent)
            parent = parent.getParentScope()
        
        for parent in reversed(parents):
            result += parent.__str__()
            result += '\n\n'

        result += self.__str__()
        print(result)
        print('================')
