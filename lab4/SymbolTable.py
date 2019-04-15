class Symbol:   # class to inherit below
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

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
