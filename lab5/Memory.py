class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):         # gets from memory current value of variable <name>
        return self.variables.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


    # def __


# pylama:ignore=W601
class MemoryStack:

    def __init__(self, memory=Memory("main")):  # initialize memory stack with memory <memory>
        self.stack = [memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack):
            value = memory.get(name)
            if value is not None:
                return value
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set_(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name, value)
                return
        self.insert(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
