from utils.predefinedTypes import *
from utils.predefinedClasses import *
from utils.predefinedFunctions import *
from utils.predefinedAttributes import *

class SymbolsTable:
    def __init__(self):
        self.classes = [IO_CLASS, OBJECT_CLASS, INT_CLASS, STRING_CLASS, BOOL_CLASS]
        self.functions = [ABORT, IN_INT, LENGTH, OUT_INT, SUBSTRING, TYPE_NAME, COPY, OUT_STRING, OUT_INT, IN_STRING, IN_INT, LENGTH, CONCAT, SUBSTRING]
        self.attributes = [OUT_STRING_ATTR, OUT_INT_ATTR, CONCAT_ATTR, SUBSTRING_START_ATTR, SUBSTRING_END_ATTR]
        self.types = [INT, STRING, BOOL, VOID, OBJECT]

    def addClass(self, Class):
        if self.findClass(Class.name) is None:
            self.classes.append(Class)
            return True
        else:
            return False

    def findClass(self, name):
        for myClass in self.classes:
            if myClass.name == name:
                return myClass
        return None

    def getFunctionWithId(self, id):
        for myFunction in self.functions:
            if myFunction.id == id:
                return myFunction
        return None

    def getFunctionWithName(self, name, isFrom):
        for myFunction in self.functions:
            if myFunction.name == name and myFunction.isFrom == isFrom:
                return myFunction
        return None

    def addFunction(self, Function):
        if self.getFunctionWithName(Function.name, Function.isFrom) is None:
            self.functions.append(Function)
            return True
        else:
            return False
    
    def AddAttribute(self, Attribute):
        if self.findAttribute(Attribute.name, Attribute.insideClass, Attribute.insideMethod, Attribute.scope) is None:
            self.attributes.append(Attribute)
            return True
        else:
            return False
    
    def findAttribute(self, name, insideClass, insideMethod, scope):
        for myAttribute in self.attributes:
            if myAttribute.name == name and myAttribute.insideClass == insideClass and myAttribute.insideMethod == insideMethod and myAttribute.scope == scope:
                return myAttribute
        return None

    def findParamsOfFunction(self, functionId):
        params = []
        for myAttribute in self.attributes:
            if myAttribute.insideMethod == functionId:
                if myAttribute.isParameterOfFunction:
                    params.append(myAttribute)
        return params

    def findNonParamsOfFunction(self, insideMethod):
        results = []
        for myAttribute in self.attributes:
            if myAttribute.insideMethod == insideMethod:
                if not myAttribute.isParameterOfFunction:
                    results.append(myAttribute)
        return results

    def addType(self, type):
        self.types.append(type)

    def findType(self, type):
        for myType in self.types:
            if myType == type:
                return myType
        return None