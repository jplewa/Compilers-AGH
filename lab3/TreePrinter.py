from __future__ import print_function
import sys
sys.path.append("..")
import lab3.AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    # @addToClass(AST.IntNum)
    # def printTree(self, indent=0):
    #     pass
    #     # fill in the body


    # @addToClass(AST.Error)
    # def printTree(self, indent=0):
    #     pass    
    #     # fill in the body

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree()

    
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(op)
        left.printTree()
        right.printTree()


    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        if self.instructions:
            for instruction in self.instructions:
                instruction.printTree()
    # define printTree for other classes
    # ...



