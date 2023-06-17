from antlr4 import *
from funxLexer import funxLexer
from funxParser import funxParser
import sys
from flask import Flask, render_template, request
if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
    from .funxVisitor import funxVisitor
else:
    from funxParser import funxParser
    from funxVisitor import funxVisitor


class TreeVisitor(funxVisitor):
    def __init__(self):
        # definedFunctions is a dictionary where the keys are the names of the
        # functions and the values are the parameters + the code of the
        # functions
        self.definedFunctions = dict()
        # stack is a vector that contains the different scopes when
        # calling several functions. The variables defined in one scope can't
        # see and can't be seen by the other scopes
        self.stack = [{}]

    def visitRootWithExpression(self, ctx):
        children = list(ctx.getChildren())
        # with children[:-2] all the children are visited except the last one (EOF)
        # and the expression
        for i in children[:-2]:
            self.visit(i)
        result = str(self.visit(children[len(children) - 2]))
        print(result)
        return result

    def visitRootWithoutExpression(self, ctx):
        children = list(ctx.getChildren())
        for i in children[:-1]:
            self.visit(i)

    def visitFunction(self, ctx):
        Scope = {
            "Params": self.visit(ctx.params),
            "Code": ctx.code
        }
        name = ctx.name.text
        if name in self.definedFunctions:
            raise Exception("Function " + name + " has been already defined")
        self.definedFunctions[name] = Scope

    def visitFunctioncall(self, ctx):
        name = ctx.name.text
        children = list(ctx.getChildren())
        if name not in self.definedFunctions:
            raise Exception("Function " + name + " hasn't been defined")
        function = self.definedFunctions[name]
        numParamDefFunction = len(function["Params"])
        numParamCalledFunction = len(children[1:])
        if numParamDefFunction != numParamCalledFunction:
            raise Exception("The number of parameters of function " + name + " doesn't match")
        i = 1
        toStack = dict()
        for param in function["Params"]:
            toStack[param] = self.visit(children[i])
            i += 1
        self.stack.append(toStack)
        result = self.visit(function["Code"])
        self.stack.pop()
        return result

    def visitParameters(self, ctx):
        children = list(ctx.getChildren())
        params = []
        for param in children:
            if param.getText() in params:
                raise Exception("The same parameter appears repeated")
            params.append(param.getText())
        return params

    def visitCodeblock(self, ctx):
        children = list(ctx.getChildren())
        for statement in children:
            res = self.visit(statement)
            if res is not None:
                return res

    def visitStatement(self, ctx):
        children = list(ctx.getChildren())
        res = self.visit(children[0])
        return res

    def visitConditional(self, ctx):
        children = list(ctx.getChildren())
        for condition in children:
            # visitIf, visitElseif and visitElse return if the condition has
            # been satisfied and the result in this case, so we can iterate
            # through the conditions
            condSat, res = self.visit(condition)
            if condSat:
                return res

    def visitIf(self, ctx):
        if (self.visit(ctx.condition) != 0):
            return True, self.visit(ctx.code)
        else:
            return False, None

    def visitElseif(self, ctx):
        if (self.visit(ctx.condition) != 0):
            return True, self.visit(ctx.code)
        else:
            return False, None

    def visitElse(self, ctx):
        return True, self.visit(ctx.code)

    def visitWhile(self, ctx):
        while (self.visit(ctx.condition) != 0):
            res = self.visit(ctx.code)
            if res is not None:
                return res

    def visitParentheses(self, ctx):
        return self.visit(ctx.expression)

    # negative powers are not defined because funx works with integers
    def visitPower(self, ctx):
        base = self.visit(ctx.base)
        exp = self.visit(ctx.exp)
        if exp < 0:
            raise Exception("Negative powers are not defined")
        return base**exp

    def visitMultDivMod(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text
        if op == '*':
            return left * right
        elif right != 0:
            if op == '/':
                return left // right
            else:
                return left % right
        else:
            raise Exception("Division by zero is illegal")

    def visitPlusMinus(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text
        if op == '+':
            return left + right
        else:
            return left - right

    def visitNegative(self, ctx):
        return -self.visit(ctx.expression)

    def visitValue(self, ctx):
        return int(ctx.val.text)

    def visitVariable(self, ctx):
        varname = ctx.var.text
        if varname not in self.stack[len(self.stack) - 1]:
            raise Exception("Variable not defined")
        return self.stack[len(self.stack) - 1][varname]

    def visitNot(self, ctx):
        return int(self.visit(ctx.expression) == 0)

    def visitAnd(self, ctx):
        right = self.visit(ctx.right)
        left = self.visit(ctx.left)
        return int((left != 0) and (right != 0) != 0)

    def visitOr(self, ctx):
        return int((self.visit(ctx.left) or self.visit(ctx.right)) != 0)

    def visitComp(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text

        if op == '>':
            return int(left > right)
        elif op == '>=':
            return int(left >= right)
        elif op == '<':
            return int(left < right)
        elif op == '<=':
            return int(left <= right)
        else:
            raise Exception("Unknown symbol")

    def visitEqDif(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = ctx.op.text

        if op == '=':
            return int(left == right)
        elif op == '!=':
            return int(left != right)
        else:
            raise Exception("Unknown symbol")

    def visitTrue(self, ctx):
        return 1

    def visitFalse(self, ctx):
        return 0

    def visitAssignment(self, ctx):
        self.stack[len(self.stack)-1][ctx.name.text] = self.visit(ctx.expression)


# app
app = Flask(__name__)
visitor = TreeVisitor()
output = []


@app.route('/')
def index():
    return render_template('base.html', output=output, functions=visitor.definedFunctions)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        try:
            input_stream = InputStream(request.form.get('input', type=str))
            lexer = funxLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = funxParser(token_stream)
            tree = parser.root()
            out = visitor.visit(tree)
            output.append(str(input_stream))
            output.append(str(out))
            if len(output) > 10:
                output.pop(0)
                output.pop(0)
        except Exception as e:
            output.append(str(input_stream))
            output.append("ERROR: " + str(e))
            if len(output) > 10:
                output.pop(0)
                output.pop(0)

    return render_template("base.html", output=output, functions=visitor.definedFunctions)
