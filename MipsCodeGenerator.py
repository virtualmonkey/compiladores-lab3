class MipsCodeGenerator:
    def __init__(
        self,
        threeAddressCode
    ):
        self.threeAddressCode = threeAddressCode
        self.mispCodeArray = []
        self.mispCodeString = ""

    def generateMipsCode(self):
        for line in self.threeAddressCode:
            if '/' in line:
                result = line.split(' = ')[0]
                assignment = line.split(' = ')[1]
                number = assignment.split(" / ")[0]
                divisor = assignment.split(" / ")[1]
                newLine = f'div {result}, {number}, {divisor}'
                self.mispCodeArray.append(newLine)
            elif '+' in line:
                result = line.split(' = ')[0]
                assignment = line.split(' = ')[1]
                operand1 = assignment.split(" + ")[0]
                operand2 = assignment.split(" + ")[1]
                newLine = f'add {result}, {operand1}, {operand2}'
                self.mispCodeArray.append(newLine)
            else:
                self.mispCodeArray.append(line)
    
    def __str__(self):
        return '\n'.join(self.mispCodeArray)
