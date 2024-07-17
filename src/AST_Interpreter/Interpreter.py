from cmp.visitor import on, when
from grammar.H_ast import *
from cmp.semantic import *
from Semantic.type_def_visitor import *
import copy
import math
import random


def Print(x):
    print(x)
    return x


def range_(min, max):
    iterable = []
    for i in range(min, max):
        iterable.append(i)
    return iterable


built_in_func = {
    "range": lambda x: range_(int(x[0]), int(x[1])),
    "print": lambda x: Print(*x),
    "sqrt": lambda x: math.sqrt(*x),
    "sin": lambda x: math.sin(*x),
    "cos": lambda x: math.cos(*x),
    "exp": lambda x: math.exp(*x),
    "log": lambda x: math.log(*reversed(x)),
    "rand": lambda: random.random(),
    "parse": lambda x: float(*x),
}


class Interpreter:
    def __init__(self, ast, Context):
        errors = []
        type_collector = typeDef(errors)
        context = Context

        self.context:Context = context

    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node:ProgramNode):
        for definition in node.definitionList:
            self.visit(definition)
        return self.visit(node.globalExpression)

    @when(DefinitionNode)
    def visit(self, node:DefinitionNode):
        pass

    @when(ExpressionNode)
    def visit(self, node:ExpressionNode):
        pass

    @when(PlusNode)
    def visit(self, node:PlusNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(MinusNode)
    def visit(self, node:MinusNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(MultiplicationNode)
    def visit(self, node:MultiplicationNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(DivisionNode)
    def visit(self, node:DivisionNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(AndNode)
    def visit(self, node:AndNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(OrNode)
    def visit(self, node:OrNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(GreaterThanNode)
    def visit(self, node:GreaterThanNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(LessThanNode)
    def visit(self, node:LessThanNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(GreaterThanEqualNode)
    def visit(self, node:GreaterThanEqualNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(LessThanEqualNode)
    def visit(self, node:LessThanEqualNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(EqualNode)
    def visit(self, node:EqualNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(NotEqualNode)
    def visit(self, node:NotEqualNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(PowerNode)
    def visit(self, node:PowerNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(IsNode)
    def visit(self, node:IsNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(AsNode)
    def visit(self, node:AsNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(ModuleNode)
    def visit(self, node:ModuleNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(ConcatSpaceNode)
    def visit(self, node:ConcatSpaceNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(ConcatNode)
    def visit(self, node:ConcatNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left, right)

    @when(NotNode)
    def visit(self, node:NotNode):
        value = self.visit(node.node)
        return not value

    @when(NegNode)
    def visit(self, node:NegNode):
        value = self.visit(node.node)
        return -value

    @when(NumberNode)
    def visit(self, node:NumberNode):
        number = node.lex
        if number == "PI":
            return math.pi
        elif number == "E":
            return math.e
        else:
            return float(node.lex)

    @when(StringNode)
    def visit(self, node:StringNode):
        return node.lex.strip('"')

    @when(BooleanNode)
    def visit(self, node:BooleanNode):
        return node.lex.lower() == 'true'

    @when(VectorNode)
    def visit(self, node:VectorNode):
        return [self.visit(element) for element in node.lex]

    @when(ExpBlockNode)
    def visit(self, node:ExpBlockNode):
        evaluation = None
        for expression in node.expLineList:
            evaluation = self.visit(expression)
        return evaluation

    @when(IndexExpNode)
    def visit(self, node:IndexExpNode):
        array = self.visit(node.factor)
        index = self.visit(node.expr)
        return array[int(index)]

    @when(IfExpNode)
    def visit(self, node:IfExpNode):
        cond = self.visit(node.cond)
        if cond:
            return self.visit(node.if_expr)
        elif node.elif_expr is not None:
            return self.visit(node.elif_expr)
        else:
            return self.visit(node.else_expr)

    @when(WhileExpNode)
    def visit(self, node:WhileExpNode):
        result = None
        while self.visit(node.cond):
            result = self.visit(node.expr)
        return result

    @when(ForExpNode)
    def visit(self, node:ForExpNode):
        result = None
        iterator = node.scope.find_variable(node.id)
        iterable = self.visit(node.expr)
        for value in iterable:
            iterator.set_value(value)
            result = self.visit(node.body)
        return result

    # region declaration
    @when(FunctionDeclNode)
    def visit(self, node:FunctionDeclNode):
        function_name = node.id
        param_names = [param.id for param in node.args]
        param_types = [self.context.get_type(str(param.type)) for param in node.args]
        return_type = self.context.get_type(str(node.return_type))
        function = self.context.create_function(function_name, param_names, param_types, None, return_type, node.body)
        return function

    @when(TypeDeclNode)
    def visit(self, node:TypeDeclNode):
        type_name = node.id
        typex = self.context.get_type(type_name)
        return typex

    @when(ProtocolDeclNode)
    def visit(self, node:ProtocolDeclNode):
        type_name = node.id
        typex = self.context.get_type(type_name)
        return typex

    @when(VariableDeclNode)
    def visit(self, node: VariableDeclNode):
        var_name = node.id
        var_type = self.context.get_type(str(node.type))
        var = node.scope.find_variable(var_name, var_type)
        value = self.visit(node.expr)
        var.set_value(value)

    @when(FunctCallNode)
    def visit(self, node:FunctCallNode):
        function_name = node.lex
        arguments = [self.visit(arg) for arg in node.args]
        if function_name in built_in_func:
            return built_in_func[function_name](tuple(arguments))
        function: Function = self.context.get_function(function_name, len(node.args))
        old_scope = copy.deepcopy(function.body.scope.parent.locals)
        body = function.body
        scope = body.scope
        for i, name in enumerate(function.param_names):
            variable = scope.find_variable(name)
            variable.set_value(arguments[i])
        result = self.visit(function.body)
        function.body.scope.parent.locals = old_scope
        return result

    @when(PropertyCallNode)
    def visit(self, node:PropertyCallNode):
        instance = node.lex.lex
        try:
            property: TypeDeclNode = node.scope.find_variable(instance).value
        except SemanticError as e:
            if instance == "self":
                method: Function = self.context.get_function(node.id, len(node.args))
                old_scope_locals = copy.deepcopy(node.scope.locals)
                for i, vname in enumerate(method.param_names):
                    value = self.visit(node.args[i])
                    node.scope.find_variable(vname).set_value(value)
                value = self.visit(method.body)
                node.scope.locals = old_scope_locals
                return value

        if isinstance(property, list):
            if node.id == "next":
                if len(property) == 0:
                    return False
                return True
            if node.id == "current":
                return property.pop(0)
        if property is None and instance == "self":
            property = node
            
            
        method: Function = self.context.get_function(node.id, len(node.args))
        old_scope_locals = copy.deepcopy(node.scope.locals)
        for i, vname in enumerate(method.param_names):
            value = self.visit(node.args[i])
            node.scope.find_variable(vname).set_value(value)
        value = self.visit(method.body)
        node.scope.locals = old_scope_locals
        return value
            

    @when(AttributeCallNode)
    def visit(self, node:AttributeCallNode):
        # value = node.scope.find_variable(node.id).value
        instance = self.context.get_type(str(node.lex))
        attribute_name = node.id
        attribute_value = instance.get_attribute(attribute_name)
        return attribute_value

    @when(VariableNode)
    def visit(self, node:VariableNode):
        var_name = node.lex
        variable = node.scope.find_variable(str(var_name))
        return variable.value

    @when(AssignExpNode)
    def visit(self, node:AssignExpNode):
        var_name = node.var.lex
        var_value = self.visit(node.expr)
        variable = node.scope.find_variable(str(var_name))
        variable.set_value(var_value)

    @when(NewExpNode)
    def visit(self, node:NewExpNode):
        type_name = node.id
        typex:Type = self.context.get_type(type_name)
        arguments = [self.visit(arg) for arg in node.args]
        for arg, attr in zip(arguments, typex.attributes):
            var:VariableInfo = node.scope.define_variable(attr.name, attr.type)
            var.set_value(arg)
        for method in typex.methods:
            self.context.create_function(method.name, method.param_names, method.param_types, method.return_type, node)
        return typex

    @when(LetExpNode)
    def visit(self, node:LetExpNode):
        for decl in node.varAssignation:
            self.visit(decl)
        result = self.visit(node.expr)
        return result

    @when(VectorIterableNode)
    def visit(self, node:VectorIterableNode):
        iterable = self.visit(node.iterable)
        result = []
        for i in iterable:
            node.expr.scope.define_variable(node.id, AutoType())
            node.expr.scope.find_variable(node.id).set_value(i)
            result.append(self.visit(node.expr))
        return result
