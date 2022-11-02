# Generated from YAPL.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

from objects.Quadruple import Quadruple
from objects.CodeCreator import CodeCreator
from objects.QuadruplesStack import QuadruplesStack


# This class defines a complete generic visitor for a parse tree produced by YAPLParser.

class ThreeAddressCodeVisitor(ParseTreeVisitor):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.codeCreator = CodeCreator()
        self.CLASS = None
        self.METHOD = None
        self.METHOD_NO = 10
        self.SCOPE = 1
        self.NEW_NO = 0

    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        return self.visit(ctx.program())


    # Visit a parse tree produced by YAPLParser#program.
    def visitProgram(self, ctx:YAPLParser.ProgramContext):
        quadruplesStack = QuadruplesStack()
        if not ctx.EOF():
            classExpr = self.visit(ctx.classExpr())
            programBlock = self.visit(ctx.program())
            quadruplesStack.addQuadruples(classExpr.quadruples)
            quadruplesStack.addQuadruples(programBlock.quadruples)
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#classExpr.
    def visitClassExpr(self, ctx:YAPLParser.ClassExprContext):
        quadruplesStack = QuadruplesStack()

        currentClassName = str(ctx.TYPE()[0])
        self.SCOPE = 1
        self.CLASS = currentClassName
        self.METHOD = None

        classQuadruple = Quadruple(
            'LBL',
            f'DECLARE_{currentClassName}',
            None
        )
        featureQuadruples = [self.visit(exprNode) for exprNode in ctx.feature()]
        
        quadruplesStack.addQuadruples([classQuadruple])
        for feature in featureQuadruples: quadruplesStack.addQuadruples(feature.quadruples)

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#method.
    def visitMethod(self, ctx:YAPLParser.MethodContext):
        quadruplesStack = QuadruplesStack()

        methodIdentifier = str(ctx.ID())
        self.METHOD_NO = self.METHOD_NO + 1
        self.SCOPE = 2

        methodQuadruple = Quadruple(
            'LBL',
            f'{methodIdentifier}∈{self.CLASS}',
            None
        )

        quadruplesStack.addQuadruples([methodQuadruple])
        
        childExpr = self.visit(ctx.expr())
        quadruplesStack.addQuadruples(childExpr.quadruples)

        returnQuadruple = Quadruple(
            '=',
            childExpr.memAddress,
            "PROCEDURE_RETURN"
        )

        quadruplesStack.addQuadruples([returnQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#attribute.
    def visitAttribute(self, ctx:YAPLParser.AttributeContext):
        quadruplesStack = QuadruplesStack()
        
        attributeIdentifier = str(ctx.ID())
        attribute = self.table.findAttribute(attributeIdentifier, self.CLASS, None, self.SCOPE)
        
        if ctx.expr():
            childExpr = self.visit(ctx.expr())
            quadruplesStack.addQuadruples(childExpr.quadruples)
            
            attributeQuadruple = Quadruple(
                '=',
                childExpr.memAddress,
                f'OBJECT_{attribute.insideClass}[{attribute.offset}]'
            )
            quadruplesStack.addQuadruples([attributeQuadruple])
        else:
            if attribute.type == "Int" or attribute.type == "Bool":
                attrQuadruple = Quadruple(
                    '=',
                    0,
                    f'OBJECT_{attribute.insideClass}[{attribute.offset}]'
                )
                quadruplesStack.addQuadruples([attrQuadruple])
            elif attribute.type == "String":
                attrQuadruple = Quadruple(
                    '=',
                    '',
                    f'OBJECT_{attribute.insideClass}[{attribute.offset}]'
                )
                quadruplesStack.addQuadruples([attrQuadruple])
            else: pass

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#formal.
    def visitFormal(self, ctx:YAPLParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#add.
    def visitAdd(self, ctx:YAPLParser.AddContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        operands = [self.visit(exprNode) for exprNode in ctx.expr()]

        for operand in operands: quadruplesStack.addQuadruples(operand.quadruples)

        addQuadruple = Quadruple(
            '+',
            operands[0].memAddress,
            temporal,
            operands[1].memAddress
        )
        quadruplesStack.addQuadruples([addQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        quadruplesStack = QuadruplesStack()

        instanceType = str(ctx.TYPE())
        myClass = self.table.findClass(instanceType)

        quadruplesStack.changeMemAddress(f'INNITIALIZE {instanceType}({self.NEW_NO})')

        newQuadruple = Quadruple(
            'MALLOC_HEAP',
            myClass.size,
            None
        )

        quadruplesStack.addQuadruples([newQuadruple])
        quadruplesStack.setType(instanceType)
        self.NEW_NO =  self.NEW_NO + 1

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#negation.
    def visitNegation(self, ctx:YAPLParser.NegationContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        negatedExpr = self.visit(ctx.expr())
        quadruplesStack.addQuadruples(negatedExpr.quadruples)

        negationQuadruple = Quadruple(
            '!=',
            negatedExpr.memAddress,
            quadruplesStack.memAddress
        )

        quadruplesStack.addQuadruples([negationQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#dispatch.
    def visitDispatch(self, ctx:YAPLParser.DispatchContext):
        quadruplesStack = QuadruplesStack()

        dispatchedExpr = [self.visit(exprNode) for exprNode in ctx.expr()]
        quadruplesStack.addQuadruples(dispatchedExpr[0].quadruples)

        methodIdentifier = str(ctx.ID())
        methodType = str(ctx.TYPE())

        if ctx.TYPE(): method = self.table.getFunctionWithName(methodIdentifier, methodType)
        else:
            mainClass = dispatchedExpr[0].getType()
            method = self.table.getFunctionWithName(methodIdentifier, mainClass) 
            if not method:
                primitiveClass = self.table.findClass(self.CLASS).inheritsFrom
                method = self.table.getFunctionWithName(methodIdentifier, primitiveClass)
        
        quadruplesStack.setType(method.type)
        
        paramsOfFunction = self.table.findParamsOfFunction(method.id)
        nonParamsOfFunction = self.table.findNonParamsOfFunction(method.id)

        allocated = 0
        for param in paramsOfFunction: allocated = allocated + param.size
        for nonParam in nonParamsOfFunction: allocated = allocated + nonParam.size

        allocateQuadruple = Quadruple(
            'MALLOC_STACK',
            allocated,
            None
        )
        quadruplesStack.addQuadruples([allocateQuadruple])

        listOfParameters = dispatchedExpr[1:]
        for x in range(len(listOfParameters)):
            if x < len(paramsOfFunction):
                quadruplesStack.addQuadruples(listOfParameters[x].quadruples)
                functionQuadruple = Quadruple(
                    '=',
                    listOfParameters[x].memAddress,
                    f'FUNCTION_{method.name}∈{method.isFrom}[{paramsOfFunction[x].offset}]'
                )
                quadruplesStack.addQuadruples([functionQuadruple])
        
        callQuadruple = Quadruple(
            'INVOKE',
            f'{method.name}∈{method.isFrom}',
            None
        )
        quadruplesStack.addQuadruples([callQuadruple])
        quadruplesStack.changeMemAddress("PROCEDURE_RETURN")
        
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        quadruplesStack = QuadruplesStack()
        
        currentString = str(ctx.STRINGS())
        quadruplesStack.changeMemAddress(currentString)
        quadruplesStack.setType("String")

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        quadruplesStack = QuadruplesStack()

        assignmentIdentifier = str(ctx.ID())
        attribute = self.table.findAttribute(assignmentIdentifier, self.CLASS, self.METHOD_NO, self.SCOPE)

        currentScope = self.SCOPE
        while currentScope  > 0:
            if attribute is None: attribute = self.table.findAttribute(assignmentIdentifier, self.CLASS, self.METHOD_NO, currentScope)
            if attribute is None: attribute = self.table.findAttribute(assignmentIdentifier, self.CLASS, None ,currentScope)
            currentScope = currentScope - 1

        childExpr = self.visit(ctx.expr())
        quadruplesStack.addQuadruples(childExpr.quadruples)

        if attribute.insideMethod:
            method = self.table.getFunctionWithId(attribute.insideMethod)
            functionQuadruple = Quadruple(
                '=',
                childExpr.memAddress,
                f'FUNCTION_{method.name}∈{attribute.insideClass}[{attribute.offset}]'
            )
            quadruplesStack.changeMemAddress(
                f'FUNCTION_{method.name}∈{attribute.insideClass}[{attribute.offset}]'
            )
            quadruplesStack.addQuadruples([functionQuadruple])
        else:
            objectQuadruple = Quadruple(
                '=',
                childExpr.memAddress,
                f'OBJECT_{attribute.insideClass}[{attribute.offset}]'
            )
            quadruplesStack.changeMemAddress(
                f'OBJECT_{attribute.insideClass}[{attribute.offset}]'
            )
            quadruplesStack.addQuadruples([objectQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#false.
    def visitFalse(self, ctx:YAPLParser.FalseContext):
        quadruplesStack = QuadruplesStack()

        currentBool = str(ctx.FALSE())
        quadruplesStack.changeMemAddress(currentBool)
        quadruplesStack.setType("Bool")

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#integer.
    def visitInteger(self, ctx:YAPLParser.IntegerContext):
        quadruplesStack = QuadruplesStack()

        currentInt = str(ctx.INTEGERS())
        quadruplesStack.changeMemAddress(currentInt)
        quadruplesStack.setType("Int")
        
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        quadruplesStack = QuadruplesStack()

        trueString, falseString, whileString = self.codeCreator.createWhile()
        ctx.inheritedAttributes = (whileString, trueString, falseString)

        childExpr = [self.visit(exprNode) for exprNode in ctx.expr()]

        whileQuadruple = Quadruple(
            'LBL',
            whileString,
            None
        )
        quadruplesStack.addQuadruples([whileQuadruple])
        quadruplesStack.addQuadruples(childExpr[0].quadruples)

        if childExpr[0].quadruples[-1].operator != "goto":
            equalQuadruple = Quadruple(
                'eq',
                childExpr[0].memAddress,
                trueString,
                1
            )
            gotoQuadruple = Quadruple(
                'goto',
                falseString,
                None
            )
            quadruplesStack.addQuadruples([equalQuadruple])
            quadruplesStack.addQuadruples([gotoQuadruple])

        trueQuadruple = Quadruple(
            'LBL',
            trueString,
            None
        )
        quadruplesStack.addQuadruples([trueQuadruple])
        quadruplesStack.addQuadruples(childExpr[1].quadruples)

        gotoQuadruple = Quadruple(
            'goto',
            whileString,
            None
        )

        falseQuadruple = Quadruple(
            'LBL',
            falseString,
            None
        )

        quadruplesStack.addQuadruples([gotoQuadruple])
        quadruplesStack.addQuadruples([falseQuadruple])
        quadruplesStack.changeMemAddress(childExpr[1].memAddress)

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#parenthesis.
    def visitParenthesis(self, ctx:YAPLParser.ParenthesisContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        quadruplesStack = QuadruplesStack()

        inheritedAtributes = ctx.parentCtx.inheritedAttributes
        childrenExpr = [self.visit(exprNode) for exprNode in ctx.expr()]

        quadruplesStack.addQuadruples(childrenExpr[0].quadruples)
        quadruplesStack.addQuadruples(childrenExpr[1].quadruples)

        equalQuadruple = Quadruple(
            'eq',
            childrenExpr[0].memAddress,
            inheritedAtributes[1],
            childrenExpr[1].memAddress
        )
        gotoQuadruple = Quadruple(
            'goto',
            inheritedAtributes[2],
            None
        )
        quadruplesStack.addQuadruples([equalQuadruple])
        quadruplesStack.addQuadruples([gotoQuadruple])
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#not.
    def visitNot(self, ctx:YAPLParser.NotContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        negatedExpr = self.visit(ctx.expr())
        quadruplesStack.addQuadruples(negatedExpr.quadruples)

        negationQuadruple = Quadruple(
            '!=',
            negatedExpr.memAddress,
            quadruplesStack.memAddress
        )

        quadruplesStack.addQuadruples([negationQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#isVoid.
    def visitIsVoid(self, ctx:YAPLParser.IsVoidContext):
        quadruplesStack = QuadruplesStack()

        quadruplesStack.changeMemAddress(self.codeCreator.createTemp())

        voidedExpr = self.visit(ctx.expr())
        quadruplesStack.addQuadruples(voidedExpr.quadruples)

        isVoidQuadruple = Quadruple(
            'void', 
            voidedExpr.memAddress,
            quadruplesStack.memAddress
        )
        quadruplesStack.addQuadruples([isVoidQuadruple])
        quadruplesStack.setType("Bool")

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#function.
    def visitFunction(self, ctx:YAPLParser.FunctionContext):
        quadruplesStack = QuadruplesStack()

        functionExprs = [self.visit(exprNode) for exprNode in ctx.expr()]

        functionIdentifier = str(ctx.ID())

        function = self.table.getFunctionWithName(functionIdentifier, self.CLASS)
        if not function:
            primitiveClass = self.table.findClass(self.CLASS)
            function = self.table.getFunctionWithName(str(functionIdentifier), primitiveClass.inheritsFrom)

        quadruplesStack.setType(function.type)

        paramsOfFunction = self.table.findParamsOfFunction(function.id)
        nonParamsOfFunction = self.table.findNonParamsOfFunction(function.id)
        
        allocated = 0
        for param in paramsOfFunction: allocated = allocated + param.size
        for nonParam in nonParamsOfFunction: allocated = allocated + nonParam.size
        
        allocateQuadruple = Quadruple(
            'MALLOC_STACK',
            allocated,
            None
        )
        quadruplesStack.addQuadruples([allocateQuadruple])
        
        for x in range(len(functionExprs)):
            if x < len(paramsOfFunction):
                quadruplesStack.addQuadruples(functionExprs[x].quadruples)
                functionQuadruple = Quadruple(
                    '=',
                    functionExprs[x].memAddress,
                    f'FUNCTION_{function.name}∈{function.isFrom}[{paramsOfFunction[x].offset}]'
                )
                quadruplesStack.addQuadruples([functionQuadruple])
        
        callQuadruple = Quadruple(
            'INVOKE',
            f'{function.name}∈{function.isFrom}',
            None
        )
        quadruplesStack.addQuadruples([callQuadruple])
        quadruplesStack.changeMemAddress("PROCEDURE_RETURN")

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        quadruplesStack = QuadruplesStack()

        inheritedAtributes = ctx.parentCtx.inheritedAttributes
        childrenExpr = [self.visit(exprNode) for exprNode in ctx.expr()]

        quadruplesStack.addQuadruples(childrenExpr[0].quadruples)
        quadruplesStack.addQuadruples(childrenExpr[1].quadruples)

        equalQuadruple = Quadruple(
            '<',
            childrenExpr[0].memAddress,
            inheritedAtributes[1],
            childrenExpr[1].memAddress
        )
        gotoQuadruple = Quadruple(
            'goto',
            inheritedAtributes[2],
            None
        )
        quadruplesStack.addQuadruples([equalQuadruple])
        quadruplesStack.addQuadruples([gotoQuadruple])
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#bracket.
    def visitBracket(self, ctx:YAPLParser.BracketContext):
        quadruplesStack = QuadruplesStack()

        bracketedQuadruples = [self.visit(exprNode) for exprNode in ctx.expr()]
        for feature in bracketedQuadruples: quadruplesStack.addQuadruples(feature.quadruples)
        
        quadruplesStack.changeMemAddress(bracketedQuadruples[-1].memAddress)
        
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#true.
    def visitTrue(self, ctx:YAPLParser.TrueContext):
        quadruplesStack = QuadruplesStack()

        currentBool = str(ctx.TRUE())
        quadruplesStack.changeMemAddress(currentBool)
        quadruplesStack.setType("Bool")

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#let.
    def visitLet(self, ctx:YAPLParser.LetContext):
        quadruplesStack = QuadruplesStack()
        self.SCOPE = self.SCOPE + 1

        childExpr = [self.visit(exprNode) for exprNode in ctx.expr()[0:-1]]
        
        for x in range(len(ctx.ID())):
            if x < len(ctx.ASIGNOPP()):
                attributeIdentifier = str(ctx.ID()[x])
                var = self.table.findAttribute(attributeIdentifier, self.CLASS, self.METHOD_NO, self.SCOPE)
                quadruplesStack.addQuadruples(childExpr[x].quadruples)
                if var.insideClass:
                    functionQuadruple = Quadruple(
                        '=',
                        childExpr[x].memAddress,
                        f'FUNCTION_{self.METHOD}∈{var.insideClass}[{var.offset}]'
                    )
                    quadruplesStack.addQuadruples([functionQuadruple])
                else:
                    objectQuadruple = Quadruple(
                        '=',
                        childExpr[x].memAddress,
                        f'OBJECT_{var.insideClass}[{var.offset}]'
                    )
                    quadruplesStack.addQuadruples([objectQuadruple])
        previous = self.visit(ctx.expr()[-1])
        quadruplesStack.addQuadruples(previous.quadruples)
        quadruplesStack.changeMemAddress(previous.memAddress)

        return quadruplesStack

    # Visit a parse tree produced by YAPLParser#divide.
    def visitDivide(self, ctx:YAPLParser.DivideContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        operands = [self.visit(exprNode) for exprNode in ctx.expr()]

        for operand in operands: quadruplesStack.addQuadruples(operand.quadruples)

        divideQuadruple = Quadruple(
            '/',
            operands[0].memAddress,
            temporal,
            operands[1].memAddress
        )

        quadruplesStack.addQuadruples([divideQuadruple])
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
        quadruplesStack = QuadruplesStack()

        variableIdentifier = str(ctx.ID())
        attribute = self.table.findAttribute(variableIdentifier, self.CLASS, self.METHOD_NO,self.SCOPE)
        
        currentScope = self.SCOPE 
        while currentScope  > 0:
            if attribute is None: attribute = self.table.findAttribute(variableIdentifier, self.CLASS, self.METHOD_NO, currentScope)
            if attribute is None: attribute = self.table.findAttribute(variableIdentifier, self.CLASS, None, currentScope)
            if attribute is not None: break
            currentScope = currentScope - 1
        
        if variableIdentifier == "self": return quadruplesStack

        if attribute.insideMethod:
            method = self.table.getFunctionWithId(attribute.insideMethod)
            quadruplesStack.changeMemAddress(f'FUNCTION_{method.name}∈{attribute.insideClass}[{attribute.offset}]')
        else: quadruplesStack.changeMemAddress(f'OBJECT_{attribute.insideClass}[{attribute.offset}]')
        quadruplesStack.setType(attribute.type)
        
        return quadruplesStack

    # Visit a parse tree produced by YAPLParser#lessEqual.
    def visitLessEqual(self, ctx:YAPLParser.LessEqualContext):
        quadruplesStack = QuadruplesStack()

        inheritedAtributes = ctx.parentCtx.inheritedAttributes
        childrenExpr = [self.visit(exprNode) for exprNode in ctx.expr()]

        quadruplesStack.addQuadruples(childrenExpr[0].quadruples)
        quadruplesStack.addQuadruples(childrenExpr[1].quadruples)

        equalQuadruple = Quadruple(
            '<=',
            childrenExpr[0].memAddress,
            inheritedAtributes[1],
            childrenExpr[1].memAddress
        )
        gotoQuadruple = Quadruple(
            'goto',
            inheritedAtributes[2],
            None
        )
        quadruplesStack.addQuadruples([equalQuadruple])
        quadruplesStack.addQuadruples([gotoQuadruple])

        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#multiply.
    def visitMultiply(self, ctx:YAPLParser.MultiplyContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        operands = [self.visit(exprNode) for exprNode in ctx.expr()]

        for operand in operands: quadruplesStack.addQuadruples(operand.quadruples)

        multiplyQuadruple = Quadruple(
            '*',
            operands[0].memAddress,
            temporal,
            operands[1].memAddress
        )

        quadruplesStack.addQuadruples([multiplyQuadruple])
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#ifElse.
    def visitIfElse(self, ctx:YAPLParser.IfElseContext):
        quadruplesStack = QuadruplesStack()

        nextString = self.codeCreator.createNext()
        trueString, falseString = self.codeCreator.createIf()
        ctx.inheritedAttributes = (nextString, trueString, falseString)

        temporal = self.codeCreator.createTemp()

        childExpr = [self.visit(exprNode) for exprNode in ctx.expr()]

        quadruplesStack.addQuadruples(childExpr[0].quadruples)

        if childExpr[0].quadruples[-1].operator != "goto":
            equalQuadruple = Quadruple(
                'eq',
                childExpr[0].memAddress,
                trueString,
                1
            )
            gotoQuadruple = Quadruple(
                'goto',
                falseString,
                None
            )
            quadruplesStack.addQuadruples([equalQuadruple])
            quadruplesStack.addQuadruples([gotoQuadruple])

        trueQuadruple = Quadruple(
            'LBL',
            trueString,
            None
        )
        quadruplesStack.addQuadruples([trueQuadruple])
        quadruplesStack.addQuadruples(childExpr[1].quadruples)

        assignQuadruple = Quadruple(
            '=',
            childExpr[1].memAddress,
            temporal
        )
        quadruplesStack.addQuadruples([assignQuadruple])

        gotoQuadruple = Quadruple(
            'goto',
            nextString,
            None
        )

        falseQuadruple = Quadruple(
            'LBL',
            falseString,
            None
        )

        quadruplesStack.addQuadruples([gotoQuadruple])
        quadruplesStack.addQuadruples([falseQuadruple])
        quadruplesStack.addQuadruples(childExpr[2].quadruples)

        assignQuadruple = Quadruple(
            '=',
            childExpr[2].memAddress,
            temporal
        )
        quadruplesStack.addQuadruples([assignQuadruple])

        labelQuadruple = Quadruple(
            'LBL',
            nextString,
            None
        )
        quadruplesStack.addQuadruples([labelQuadruple])
        quadruplesStack.changeMemAddress(temporal)
        return quadruplesStack


    # Visit a parse tree produced by YAPLParser#substract.
    def visitSubstract(self, ctx:YAPLParser.SubstractContext):
        quadruplesStack = QuadruplesStack()

        temporal = self.codeCreator.createTemp()
        quadruplesStack.changeMemAddress(temporal)

        operands = [self.visit(exprNode) for exprNode in ctx.expr()]

        for operand in operands: quadruplesStack.addQuadruples(operand.quadruples)

        substractQuadruple = Quadruple(
            '-',
            operands[0].memAddress,
            temporal,
            operands[1].memAddress
        )

        quadruplesStack.addQuadruples([substractQuadruple])
        return quadruplesStack



del YAPLParser