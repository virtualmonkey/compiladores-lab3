# code extracted from https://github.com/GabrielBMiranda/MiniJava_Compiler/blob/6e56fc290375adb3ac1812570a1e4b3f0522cff4/IR_PAI/UnaryAssignmentIR.py

from utils.consts.consts import labelInterpreter
class Quadruple():
    def __init__(
        self, 
        operator, 
        arg1, 
        result, 
        arg2 = None
    ):
        self.operator = operator
        self.arg1 = arg1
        self.result = result
        self.arg2 = arg2
    
    def __str__(self):
        return labelInterpreter(
            self.operator,
            self.arg1,
            self.result,
            self.arg2
        )
