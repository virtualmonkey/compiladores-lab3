from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor

# This class defines a complete generic visitor for a parse tree produced by YAPLParser.
from objects.Attribute import Attribute
from objects.Error import Error


from tables.SymbolsTable import *

class MyYAPLNewVisitor(YAPLVisitor):
    def __init__(self, table, errors):
        super().__init__()
        self.table = table
        self.errors = errors
        self.CLASS = ""
        self.METHOD = ""
        self.METHOD_NO = 10
        self.SCOPE = 1

    def getInheritance(self, givenClass, wantedClass):
        if not givenClass:
            return False
        parent = self.table.findClass(givenClass.inheritsFrom)
        family = []
        while parent:
            family.append(parent.name)
            parent = self.table.findClass(parent.inheritsFrom)
        if wantedClass not in family: return False
        else: return True

    def buildErrorString(self):
        if not self.table.findClass("Main"):
            self.errors.append(
                Error(
                    "SyntaxError",
                    "0",
                    "YAPL programs must have a Main class"
                )
            )
        else: 
            if not self.table.getFunctionWithName("main", "Main"):
                self.errors.append(
                    Error(
                        "SyntaxError",
                        "0",
                        "Main class must have a main method"
                    )
                )

            if self.table.findClass("Main").inheritsFrom != None and self.table.findClass("Main").inheritsFrom != 'IO':
                self.errors.append(
                    Error(
                        "SyntaxError",
                        "1",
                        "Main class can't inherit from any other class"
                    )
                )
        
        stringOfErrors = ''

        if len(self.errors) > 0:
            for myError in self.errors:
                stringOfErrors += str(myError) + "\n"
        else:
            stringOfErrors += "Compiled successfully!"

        return stringOfErrors

    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#program.
    def visitProgram(self, ctx:YAPLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#classExpr.
    def visitClassExpr(self, ctx:YAPLParser.ClassExprContext):
        classIdentifier = str(ctx.TYPE()[0])
        self.CLASS = classIdentifier
        self.METHOD = None
        self.SCOPE = 1
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#method.
    def visitMethod(self, ctx:YAPLParser.MethodContext):
        self.METHOD_NO = self.METHOD_NO + 1
        
        methodIdentifier = str(ctx.ID())
        methodType = str(ctx.TYPE())

        self.SCOPE = 2

        if methodType == "SELF_TYPE": methodType = self.CLASS

        self.METHOD = methodIdentifier
        for node in ctx.formal(): self.visit(node)

        result = self.visit(ctx.expr())
        if result == "SELF_TYPE": result = self.CLASS

        elif result == methodType or self.getInheritance(self.table.findClass(result), methodType): return methodType

        else:
            error = Error(
                        "TypeError",
                        ctx.ID().getPayload().line,
                        "method '" + methodIdentifier + "' returns '" + result + "' instead of '" + methodType + "'"
                    ) if result else Error(
                        "TypeError",
                        ctx.ID().getPayload().line,
                        "method '" + methodIdentifier + "' doesn't return anything but '" + methodType + "' was expected"
                    )
            self.errors.append(error)
            return "Error"


    def visitAttribute(self, ctx:YAPLParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#formal.
    def visitFormal(self, ctx:YAPLParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#add.
    def visitAdd(self, ctx:YAPLParser.AddContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        if operands[0] == "Int" and operands[-1] == "Int":
            return "Int"
        elif operands[0] == "String" and operands[-1] == "String":
            return "String"
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "cannot add '" + operands[0] + "' and '" + operands[-1] + "'"
                )
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        classType = str(ctx.TYPE())

        if self.table.findClass(classType): return classType

        else:
            if self.table.findType(classType): return classType

            else:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.start.line,
                        "class or type '" + classType + "' is not defined"
                    )
                )
                return "Error"


    # Visit a parse tree produced by YAPLParser#negation.
    def visitNegation(self, ctx:YAPLParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatch.
    def visitDispatch(self, ctx:YAPLParser.DispatchContext):
        visitedNodes = []

        for epressionNode in ctx.expr():
            visited = self.visit(epressionNode)
            if visited == "SELF_TYPE": visited = self.CLASS
            visitedNodes.append(visited)

        mainClass = visitedNodes[0]
        parentClass = ""

        if ctx.TYPE():
            parentClass = str(ctx.TYPE())

            if not self.table.findClass(parentClass):
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "Class '" + parentClass + "' not defined"
                    )
                )
                return "Error"
            myClass = self.table.findClass(mainClass)

            if myClass is None:
                self.errors.append(
                     Error(
                        "SyntaxError",
                        ctx.ID().getPayload().line,
                        "Can't call method of type Error"
                    )
                )
                return "Error"

            if myClass.inheritsFrom != parentClass:
                parent = self.table.findClass(myClass.inheritsFrom)
                family = []
                while parent:
                    family.append(parent.name)
                    parent = self.table.findClass(parent.inheritsFrom)         
                if parentClass not in family:
                    self.errors.append(
                        Error(
                            "UnreachableMethod",
                            ctx.ID().getPayload().line,
                            "class " + mainClass + " can't acces methods from class '" + parentClass + "'")
                    )
                    return "Error"

            myMethod =  self.table.getFunctionWithName(str(ctx.ID()), parentClass)
            if myMethod:
                parameters = visitedNodes[1:]
                firmParameters = self.table.findParamsOfFunction(myMethod.id)
                if len(parameters) != len(firmParameters):
                    self.errors.append(
                        Error(
                            "ParamOverflowError",
                            ctx.ID().getPayload().line,
                            "function '" + myMethod.name + "' expects " + str(len(firmParameters)) + " parameters but instead '" + str(len(parameters)) + "' were given")
                    )
                    return "Error"
                for x in range(len(parameters)):
                    if parameters[x] != firmParameters[x].type:
                        self.errors.append(
                            Error(
                                "TypeError",
                                ctx.ID().getPayload().line,
                                "function '" + myMethod.name + "' expects parameter of type '" + firmParameters[x].type + "' in order " + str(x+1) + " but was given '" + parameters[x] + "'"
                            )
                        )
                        return "Error"
                if myMethod.type == "SELF_TYPE": return visitedNodes[0]
                else: return myMethod.type
            else:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "method '" + str(ctx.ID()) + "' wasn't declared in class '" + parentClass + "'")
                )
                return "Error"
        else:
            myMethod = self.table.getFunctionWithName(str(ctx.ID()), mainClass)
            if myMethod:
                parameters = visitedNodes[1:]
                firmParameters = self.table.findParamsOfFunction(myMethod.id)
                if len(parameters) != len(firmParameters):
                    self.errors.append(
                        Error(
                            "ParamOverflowError",
                            ctx.ID().getPayload().line,
                            "function '" + myMethod.name + "' expects " + str(len(firmParameters)) + " parameters but instead '" + str(len(parameters)) + "' were given"
                            )
                    )
                    return "Error"
                for x in range(len(parameters)):
                    if parameters[x] != firmParameters[x].type:
                        self.errors.append(
                            Error(
                                "TypeError",
                                ctx.ID().getPayload().line,
                                "function '" + myMethod.name + "' expects parameter of type '" + firmParameters[x].type + "' in order " + str(x+1) + " but was given '" + parameters[x] + "'"
                            )
                        )
                        return "Error"
                if myMethod.type == "SELF_TYPE": return visitedNodes[0]
                else: return myMethod.type
            else:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "method '" + str(ctx.ID()) + "' wasn't declared in class '" + parentClass + "'")
                )
                return "Error"


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return "String"


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        attributeName = str(ctx.ID())

        attribute = self.table.findAttribute(attributeName, self.CLASS, self.METHOD_NO,self.SCOPE)
        
        currentScope = self.SCOPE  

        while currentScope  > 0:
            if attribute is None:
                attribute = self.table.findAttribute(attributeName, self.CLASS, self.METHOD_NO ,currentScope)
            if attribute is None:
                attribute = self.table.findAttribute(attributeName, self.CLASS, None ,currentScope)
            currentScope = currentScope - 1

        if attribute is None:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.ID().getPayload().line,
                    "variable '" + attributeName + "' not found"
                )
            )
            return "Error"

        assignment = self.visit(ctx.expr())
        if assignment == attribute.type or self.getInheritance(self.table.findClass(assignment), attribute.type): return attribute.type

        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.ID().getPayload().line,
                    "Can't assign '" + assignment + "' to '" + attribute.type + "'"
                )
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#false.
    def visitFalse(self, ctx:YAPLParser.FalseContext):
        return "Bool"


    # Visit a parse tree produced by YAPLParser#integer.
    def visitInteger(self, ctx:YAPLParser.IntegerContext):
        return "Int"


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        condition = [self.visit(operand) for operand in ctx.expr()]

        if condition[0] == "Bool": return "Object"
        else:
            self.errors.append(
                Error(
                    "WrongCondition",
                    ctx.start.line,
                    "can't use type '" + condition[0] + "' as a condition for a while loop"
                )
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#parenthesis.
    def visitParenthesis(self, ctx:YAPLParser.ParenthesisContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        # Case Int
        if operands[0] == "Int" and operands[1] == "Int": return "Bool"
        elif operands[0] == "Int" and operands[1] == "String": return "Bool"
        elif operands[0] == "String" and operands[1] == "Int": return "Bool"
        elif operands[0] == "Bool" and operands[1] == "Int": return "Bool"
        elif operands[0] == "Int" and operands[1] == "Bool": return "Bool"

        # Case String
        elif operands[0] == "String" and operands[1] == "String": return "Bool"
        elif operands[0] == "String" and operands[1] == "Bool": return "Bool"
        elif operands[0] == "Bool" and operands[1] == "String": return "Bool"

        # Case Bool
        elif operands[0] == "Bool" and operands[1] == "Bool": return "Bool"

        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "Cannot compare types '" + operands[0] + "' and '" + operands[1] + "'"
                    )
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#not.
    def visitNot(self, ctx:YAPLParser.NotContext):
        operand = self.visit(ctx.expr())
        if operand == "Bool" or operand == "Int": return operand
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "cannot perform not operation on type '" + operand + "'")
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#isVoid.
    def visitIsVoid(self, ctx:YAPLParser.IsVoidContext):
        return "Bool"


    # Visit a parse tree produced by YAPLParser#function.
    def visitFunction(self, ctx:YAPLParser.FunctionContext):
        visitedNodes = []

        for expressionNode in ctx.expr():
            childresult = self.visit(expressionNode)
            if childresult == "SELF_TYPE": childresult = self.CLASS
            visitedNodes.append(childresult)

        myMethod = self.table.getFunctionWithName(str(ctx.ID()), self.CLASS)
        if myMethod:
            firmParameters = self.table.findParamsOfFunction(myMethod.id)
            if len(visitedNodes) != len(firmParameters):
                self.errors.append(Error("ParamOverflow", ctx.ID().getPayload().line, "function '" + myMethod.name + "' expects " + str(len(firmParameters)) + " parameters but instead '" + str(len(visitedNodes)) + "' were given"))
                return "Error"
            for x in range(len(visitedNodes)):
                if visitedNodes[x] != firmParameters[x].type:
                    self.errors.append(Error("TypeError", ctx.ID().getPayload().line, "function " + myMethod.name + " expects parameter of type '" + firmParameters[x].type + "' in order " + str(x+1) + " but was given '" + visitedNodes[x] + "'"))
                    return "Error"
            if myMethod.type == "SELF_TYPE":
                return visitedNodes[0]
            else:
                return myMethod.type
        else:
            usingClass = self.table.findClass(self.CLASS)
            if usingClass:
                parrentClass = usingClass.inheritsFrom

                if parrentClass:

                    myMethod = self.table.getFunctionWithName(str(ctx.ID()), parrentClass)
                    if myMethod:
                        firmParameters = self.table.findParamsOfFunction(myMethod.id)
                        if len(visitedNodes) != len(firmParameters):
                            self.errors.append(Error("ParamOverflow", ctx.ID().getPayload().line, "function '" + myMethod.name + "' expects " + str(len(firmParameters)) + " parameters but instead '" + str(len(visitedNodes)) + "' were given"))
                            return "Error"
                        for x in range(len(visitedNodes)):
                            if visitedNodes[x] != firmParameters[x].type:
                                self.errors.append(Error("TypeError", ctx.ID().getPayload().line, "function " + myMethod.name + " expects " + firmParameters[x].type + " as parameter " + str(x+1) + " but " + visitedNodes[x] + " was given"))
                                return "Error"
                        if myMethod.type == "SELF_TYPE": return visitedNodes[0]
                        else: return myMethod.type
                    else:
                        self.errors.append(Error("NameError", ctx.ID().getPayload().line, "function " + str(ctx.ID()) + " not defined"))
                        return "Error"
                else:
                    self.errors.append(Error("NameError", ctx.ID().getPayload().line, "function " + str(ctx.ID()) + " not defined"))
                    return "Error"
            else:
                return "Error"


    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        if operands[0] == "Int" and operands[1] == "Int": return "Bool"
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "cannot compare types '" + operands[0] + "' and '" + operands[1] + "'")
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#bracket.
    def visitBracket(self, ctx:YAPLParser.BracketContext):
        operands = [self.visit(operand) for operand in ctx.expr()]
        
        if len(operands) == 0:
            self.errors.append(
                Error(
                    "EmptyBracket",
                    ctx.start.line,
                    "Brackets must contain at least one expression")
            )
            return "Error"
        return operands[-1]


    # Visit a parse tree produced by YAPLParser#true.
    def visitTrue(self, ctx:YAPLParser.TrueContext):
        return "Bool"


    # Visit a parse tree produced by YAPLParser#let.
    def visitLet(self, ctx:YAPLParser.LetContext):
        self.SCOPE = self.SCOPE + 1

        assignments = ctx.expr()[0:-1]
        assignmentTypes = [ self.visit(node) for node in assignments]

        for x in range(len(ctx.ID())):
            newVariableType = str(ctx.TYPE()[x])
            if x < len(assignmentTypes):
                if assignmentTypes[x] != newVariableType:
                    self.errors.append(
                        Error(
                            "TypeError",
                            ctx.ID().getPayload().line,
                            "can't assign type '" + assignmentTypes[x] + "' to type '" + newVariableType + "'")
                    )
                    return "Error"
        lastAssignment = self.visit(ctx.expr()[-1])
        self.SCOPE = self.SCOPE - 1
        return lastAssignment


    # Visit a parse tree produced by YAPLParser#divide.
    def visitDivide(self, ctx:YAPLParser.DivideContext):
        operands = [self.visit(operand) for operand in ctx.expr()]
        
        if operands[0] == "Int" and operands[-1] == "Int": return "Int"

        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "Cannot divide '" + operands[0] + "' and '" + operands[-1] + "'")
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
        variableIdentifier = str(ctx.ID())
        if variableIdentifier == "self": return "SELF_TYPE"

        else:
            attribute = self.table.findAttribute(variableIdentifier, self.CLASS, self.METHOD_NO,self.SCOPE)
            scope = self.SCOPE 
            while scope  > 0:
                if attribute is None: attribute = self.table.findAttribute(variableIdentifier, self.CLASS, self.METHOD_NO ,scope)
                if attribute is None: attribute = self.table.findAttribute(variableIdentifier, self.CLASS, None ,scope)
                if attribute is not None: return attribute.type
                scope = scope - 1

            if attribute is None:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "variable '" + variableIdentifier + "' not found"
                    )
                )
                return "Error"


    # Visit a parse tree produced by YAPLParser#lessEqual.
    def visitLessEqual(self, ctx:YAPLParser.LessEqualContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        if operands[0] == "Int" and operands[1] == "Int":
            return "Bool"
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "Cannot compare types '" + operands[0] + "' and '" + operands[1] + "'")
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#multiply.
    def visitMultiply(self, ctx:YAPLParser.MultiplyContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        if operands[0] == "Int" and operands[-1] == "Int":
            return "Int"
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "Cannot multiply " + operands[0] + " and " + operands[-1]
                )
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#ifElse.
    def visitIfElse(self, ctx:YAPLParser.IfElseContext):
        operands = [self.visit(operand) for operand in ctx.expr()]
    
        if operands[0] == "Bool":
            if operands[1] == operands[2]:
                return operands[1]
            return "Object"

        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "conditional of if must return 'Boolean' instead of '" + operands[0] + "'")
            )
            return "Error"


    # Visit a parse tree produced by YAPLParser#substract.
    def visitSubstract(self, ctx:YAPLParser.SubstractContext):
        operands = [self.visit(operand) for operand in ctx.expr()]

        if operands[0] == "Int" and operands[-1] == "Int":
            return "Int"
        else:
            self.errors.append(
                Error(
                    "TypeError",
                    ctx.start.line,
                    "cannot substract '" + operands[0] + "' and '" + operands[-1] + "'"
                )
            )
            return "Error"




del YAPLParser