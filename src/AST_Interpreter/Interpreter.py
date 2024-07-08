from cmp.visitor import on, when
from grammar.H_ast import *
from cmp.semantic import *
from Semantic.type_def_visitor import *

def Print(x):
    print(x)
    return x
built_in_func = {
    "print": lambda x: Print(*x),
    # "sqrt": lambda x: math.sqrt(*x),
    # "sin": lambda x: math.sin(*x),
    # "cos": lambda x: math.cos(*x),
    # "exp": lambda x: math.exp(*x),
    # "log": lambda x: math.log(*reversed(x)),
    # "rand": lambda: random.random(),
    "parse": lambda x: float(*x),
}

class Interpreter:
    def __init__(self,ast):
        errors=[]
        type_collector = typeDef(errors)
        context, errors = type_collector.visit(ast)
        

        self.context = context
    
    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node):
        for definition in node.definitionList:
            self.visit(definition)
        return self.visit(node.globalExpression)
    
    @when(DefinitionNode)
    def visit(self, node):
        pass
    @when(ExpressionNode)
    def visit(self, node):
        pass

    @when(PlusNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(MinusNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(MultiplicationNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(DivisionNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(AndNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(OrNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(GreaterThanNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(LessThanNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(GreaterThanEqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(LessThanEqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(EqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)

    @when(NotEqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(PowerNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(IsNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(AsNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(ModuleNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    
    @when(ConcatSpaceNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)
    @when(ConcatNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node.operate(left,right)


    
    @when(NotNode)
    def visit(self, node):
        value = self.visit(node.node)
        return not value

    @when(NegNode)
    def visit(self, node):
        value = self.visit(node.node)
        return -value
    
    
    @when(NumberNode)
    def visit(self, node):
        return int(node.lex)
    
    @when(StringNode)
    def visit(self, node):
        return node.lex.strip('"')
    
    @when(BooleanNode)
    def visit(self, node):
         return node.lex.lower() == 'true'
    
    @when(VectorNode)
    def visit(self, node):
        return [self.visit(element) for element in node.lex]
    
    @when(ExpBlockNode)
    def visit(self, node):
        evaluation = None
        for expression in node.expLineList:
            evaluation = self.visit(expression)
        return evaluation
    
    @when(IndexExpNode)
    def visit(self, node):
        array = self.visit(node.factor)
        index = self.visit(node.expr)
        return array[index]

    @when(IfExpNode)
    def visit(self, node):
        cond = self.visit(node.cond)
        if cond:
            return self.visit(node.if_expr)
        elif node.elif_expr is not None:
            return self.visit(node.elif_expr)
        else:
            return self.visit(node.else_expr)
    
    @when(WhileExpNode)
    def visit(self, node):
        while self.visit(node.cond):
            self.visit(node.expr)
    
    @when(ForExpNode)
    def visit(self, node):
        iterable = self.visit(node.expr)
        for value in iterable:
            self.visit(node.body)
        
    # region declaration
    @when(FunctionDeclNode)
    def visit(self, node):
        function_name = node.id
        param_names = [param.id for param in node.args]
        param_types = [self.context.get_type(str(param.type)) for param in node.args]
        return_type = self.context.get_type(str(node.return_type))
        function = self.context.create_function(function_name, param_names, param_types,None, return_type,node.body)
        return function
    @when(TypeDeclNode)
    def visit(self, node):
        type_name = node.id
        typex = self.context.get_type(type_name)
        return typex
    
    @when(ProtocolDeclNode)
    def visit(self, node):
        type_name = node.id
        typex = self.context.get_type(type_name)
        return typex
    @when(VariableDeclNode)
    def visit(self, node:VariableDeclNode):
        value = self.visit(node.expr)
        var_name = node.id
        var_type = self.context.get_type(str(node.type))
        var=node.scope.find_variable(var_name, var_type)
        var.set_value(value)
    

    @when(FunctCallNode)
    def visit(self, node):
        function_name = node.lex
        arguments = [self.visit(arg) for arg in node.args]
        if function_name in built_in_func:
            return built_in_func[function_name](tuple(arguments))
        function: Function = self.context.get_function(function_name)
        body= function.body
        scope=body.scope
        for i, name in enumerate(function.param_names):
            variable = scope.find_variable(name)
            variable.set_value(arguments[i])
        return self.visit(function.body)
    @when(PropertyCallNode)
    def visit(self, node):
        instance = self.visit(node.lex)                        #!Duda
        property_name = node.id
        property_value = instance.get_property(property_name)
        return property_value
    @when(AttributeCallNode)
    def visit(self, node):
        instance = self.visit(node.lex)
        attribute_name = node.id
        attribute_value = instance.get_attribute(attribute_name)
        return attribute_value

    
    @when(VariableNode)
    def visit(self, node):
       var_name = node.lex
       variable = node.scope.find_variable(str(var_name))
       return variable.value

    @when(AssignExpNode)
    def visit(self, node):
        var_name = node.var
        var_value = self.visit(node.expr)
        variable = self.current_scope.find_variable1(var_name)
        variable.value = var_value
    
    @when(NewExpNode)
    def visit(self, node):
        type_name = node.id
        typex = self.context.get_type(type_name)
        arguments = [self.visit(arg) for arg in node.args]
        instance = typex(*arguments)
        return instance
    
    @when(LetExpNode)
    def visit(self, node):
        # new_scope = self.current_scope.create_child()
        # self.current_scope = new_scope
        for decl in node.varAssignation:
            self.visit(decl)
        result = self.visit(node.expr)
        # self.current_scope = self.current_scope.parent
        return result
    @when(VectorIterableNode)
    def visit(self, node):
        # Implementar la lógica para vector iterable
        pass

    
   

   

    

   

   
   



    

   

   

    

    

    




