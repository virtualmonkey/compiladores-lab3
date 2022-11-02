class CodeCreator():
    def __init__(self):
        self.tempControl = 0
        self.ifControl = 0
        self.nextControl = 0
        self.whileControl = 0
    
    def createTemp(self):
        self.tempControl +=1
        return f't{self.tempControl}'

    def createNext(self):
        self.nextControl += 1
        return f'[{self.nextControl - 1}]NEXT' 
    
    def createIf(self):
        self.ifControl += 1
        return f'[{self.ifControl - 1}]IF_TRUE', f'[{self.ifControl - 1}]IF_FALSE'

    def createWhile(self):
        self.whileControl +=1
        return f'[{self.whileControl - 1}]WHILE_TRUE', f'[{self.whileControl - 1}]WHILE_FALSE', f'[{self.whileControl - 1}]WHILE'