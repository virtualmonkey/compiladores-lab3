class QuadruplesStack():
    def __init__(self):
        self.quadruples = []
        self.memAddress = 't0'
        self.type = None
        self.attrs = None

    def __str__(self):
        stringQuadruples = [str(quadruple) for quadruple in self.quadruples]
        return '\n'.join(stringQuadruples)

    def setAttrs(self, attrs): self.attrs = attrs

    def setType(self, type): self.type = type

    def getType(self): return self.type

    def addQuadruples(self, quadruples: list):
        for quadruple in quadruples: self.quadruples.append(quadruple)
        
    def changeMemAddress(self, memAddress:str): self.memAddress = memAddress
