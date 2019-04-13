class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.type = "binexpr"
        self.op = op
        self.left = left
        self.right = right


# ...
# fill out missing classes
# ...

class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions if instructions else []
    # def __repr__(self):
    #     return '{}'.format(self.instructions) if self.instructions else ''

class Instructions(Node):
    def __init__(self, instruction):
        self.instructions = [instruction]
    
    def addInstruction(self, instruction):
        self.instructions.append(instruction)


class Error(Node):
    def __init__(self):
        pass
