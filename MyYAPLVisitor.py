from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor

# This class defines a complete generic visitor for a parse tree produced by YAPLParser.
from objects.Class import Class
from objects.Function import Function
from objects.Attribute import Attribute
from objects.Error import Error

from utils.predefinedTypes import *
from tables.SymbolsTable import *

class MyYAPLVisitor(YAPLVisitor):
    def __init__(self):
        super().__init__()
        self.table = SymbolsTable()
        self.errors = []
        self.CLASS = ""
        self.METHOD = ""
        self.METHOD_NO = 10
        self.SCOPE = 1
        self.OFFSET = 0
        self.primitiveTypesSizes = PRIMITIVE_TYPE_SIZES

    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#program.
    def visitProgram(self, ctx:YAPLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#classExpr.
    def visitClassExpr(self, ctx:YAPLParser.ClassExprContext):
        classIdentifier = str(ctx.TYPE()[0])
        classParents = ctx.TYPE()
        if len(classParents) > 1:
            inheritedClass = str(classParents[1])
            if (inheritedClass == classIdentifier):
                self.errors.append(
                    Error(
                        "SyntaxError",
                        ctx.start.line,
                        "Class can't inherit from itself"
                    )
                )
                return "Error"
            
            if (inheritedClass == "Int" or inheritedClass == "Bool" or inheritedClass == "String"):
                self.errors.append(
                    Error(
                        "TypeError",
                        ctx.start.line,
                        "Class can't inherit from primitive types"
                    )
                )
                return "Error"
            
            if not self.table.findClass(inheritedClass):
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.start.line,
                        "class '" + inheritedClass + "' is not defined"
                    )
                )
                return "Error"

        else: inheritedClass = None

        self.CLASS = classIdentifier
        self.METHOD = None
        self.SCOPE = 1
        self.OFFSET = 0

        children = [self.visit(node) for node in ctx.feature()]
        
        newClass = Class(classIdentifier, inheritedClass, size = sum(children)) if inheritedClass else Class(classIdentifier, size = sum(children))
        addition = self.table.addClass(newClass)

        if not addition:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.start.line,
                    "class '" + classIdentifier + "' has already been defined in current scope"
                )
            )
            return "Error"

    # Visit a parse tree produced by YAPLParser#method.
    def visitMethod(self, ctx:YAPLParser.MethodContext):
        self.METHOD_NO = self.METHOD_NO + 1

        methodIdentifier = str(ctx.ID())
        methodType = str(ctx.TYPE())
        
        addition = self.table.addFunction(
            Function(
                self.METHOD_NO,
                methodIdentifier,
                methodType,
                self.SCOPE,
                self.CLASS
            )
        )
        
        self.SCOPE = 2
        if not addition:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.ID().getPayload().line,
                    "method '" + methodIdentifier + "' has already been defined in current scope"
                )
            )
            return "Error"
        else:
            self.METHOD = methodIdentifier
            self.OFFSET = 0
            for child in ctx.formal(): self.visit(child)
            self.visit(ctx.expr())
            return 0


    # Visit a parse tree produced by YAPLParser#attribute.
    def visitAttribute(self, ctx:YAPLParser.AttributeContext):
        attributeIdentifier = str(ctx.ID())
        attributeType = str(ctx.TYPE())

        size = self.primitiveTypesSizes[attributeType] if attributeType in self.primitiveTypesSizes else 1

        if self.METHOD:
            newAttribute = Attribute(attributeIdentifier, attributeType, self.SCOPE, self.CLASS, self.METHOD_NO, size = size, offset = self.OFFSET)
            self.OFFSET += size
        else:
            newAttribute = Attribute(attributeIdentifier, attributeType, self.SCOPE, self.CLASS, None, size = size, offset = self.OFFSET)
            self.OFFSET += size

        addition = self.table.AddAttribute(newAttribute)

        if not addition:
            self.errors.append(
                 Error(
                    "NameError",
                    ctx.ID().getPayload().line,
                    "attribute '" + attributeIdentifier + "' has already been defined in current scope"
                    )
            )
            return "Error"
        else:
            self.visitChildren(ctx)
            return size


    # Visit a parse tree produced by YAPLParser#formal.
    def visitFormal(self, ctx:YAPLParser.FormalContext):
        parameterIdentifier = str(ctx.ID())
        parameterType = str(ctx.TYPE())

        size = self.primitiveTypesSizes[parameterType] if parameterType in self.primitiveTypesSizes else 1

        newAttribute = Attribute(
                parameterIdentifier,
                parameterType,
                self.SCOPE,
                self.CLASS,
                self.METHOD_NO,
                True,
                size,
                self.OFFSET
            )

        self.OFFSET += size
        addition = self.table.AddAttribute(newAttribute)
        
        if not addition:
            self.errors.append(
                Error(
                    "NameError",
                    ctx.ID().getPayload().line,
                    "parameter '" + parameterIdentifier + "' already defined"
                )
            )
            return "Error"
        else:
            return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#add.
    def visitAdd(self, ctx:YAPLParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#negation.
    def visitNegation(self, ctx:YAPLParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatch.
    def visitDispatch(self, ctx:YAPLParser.DispatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#false.
    def visitFalse(self, ctx:YAPLParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#integer.
    def visitInteger(self, ctx:YAPLParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#parenthesis.
    def visitParenthesis(self, ctx:YAPLParser.ParenthesisContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#not.
    def visitNot(self, ctx:YAPLParser.NotContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#isVoid.
    def visitIsVoid(self, ctx:YAPLParser.IsVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#function.
    def visitFunction(self, ctx:YAPLParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#bracket.
    def visitBracket(self, ctx:YAPLParser.BracketContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#true.
    def visitTrue(self, ctx:YAPLParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#let.
    def visitLet(self, ctx:YAPLParser.LetContext):
        self.SCOPE = self.SCOPE + 1

        for x in range(len(ctx.ID())):
            newVariableIdentifier = str(ctx.ID()[x])
            newVariableType = str(ctx.TYPE()[x])
            size = self.primitiveTypesSizes[newVariableType] if newVariableType in self.primitiveTypesSizes else 1
            
            addition = self.table.AddAttribute(
                Attribute(
                    newVariableIdentifier,
                    newVariableType,
                    self.SCOPE,
                    self.CLASS,
                    self.METHOD_NO,
                    size = size,
                    offset = self.OFFSET
                )
            )

            self.OFFSET += size

            if not addition:
                self.errors.append(
                    Error(
                        "NameError",
                        ctx.ID().getPayload().line,
                        "variable " + newVariableIdentifier + " has already been defined in current scope"
                    )
                )
                return "Error"
        self.visit(ctx.expr()[-1])
        self.SCOPE = self.SCOPE - 1
        return 0


    # Visit a parse tree produced by YAPLParser#divide.
    def visitDivide(self, ctx:YAPLParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessEqual.
    def visitLessEqual(self, ctx:YAPLParser.LessEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#multiply.
    def visitMultiply(self, ctx:YAPLParser.MultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#ifElse.
    def visitIfElse(self, ctx:YAPLParser.IfElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#substract.
    def visitSubstract(self, ctx:YAPLParser.SubstractContext):
        return self.visitChildren(ctx)




del YAPLParser