from cmp.visitor import *
from cmp.semantic import *
from cmp.semantic import *
from grammar.H_ast import *
from Tools.errors import *


class type_inference:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.object_type = self.context.get_type("Object")
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for definition in node.definitionList:
            self.visit(definition)
        self.visit(node.globalExpression)
        return self.context, self.errors

    @visitor.when(TypeDeclNode)
    def visit(self, node):
        if node.id.startswith('<error>'):
            return
        # scope = scope.create_child()
        self.current_type = self.context.get_type(str(node.id))

        if node.args != None:
            if (len(node.args) == 0) and (node.parents != None):
                node.args = self.context.get_type(str(node.parents)).attributes
                for arg in node.args:
                    try:
                        self.current_type.define_attribute(arg, self.context.get_type(str(arg)))
                        node.scope.parent.define_variable(arg, self.context.get_type(str(arg)))
                    except SemanticError as e:
                        self.current_type.define_attribute(arg, self.object_type)
                        node.scope.parent.define_variable(arg, self.object_type)
            else:
                for arg in node.args:
                    add = True
                    if arg.id in [at.name for at in self.current_type.attributes]:
                        add = False
                    try:
                        if add:
                            self.current_type.define_attribute(arg, self.context.get_type(str(arg)))
                        node.scope.parent.define_variable(arg.id, self.context.get_type(str(arg.id)))
                    except SemanticError as e:
                        if add:
                            self.current_type.define_attribute(arg.id, self.object_type)
                        try:
                            node.scope.parent.define_variable(arg.id, self.object_type)
                        except Exception as e:
                            pass

        if self.current_type.parent:
            parent_type = self.current_type.parent
            if type(parent_type) == ErrorType():
                self.errors.append(errors(node.line, 0, f'Invalid parent type for "{node.id}"', "SEMANTIC ERROR"))

        for attribute in node.attributes:
            self.visit(attribute)

        self.current_type = None

    @visitor.when(ProtocolDeclNode)
    def visit(self, node):
        if node.id.startswith('<error>'):
            return
        # scope = scope.create_child()
        self.current_type = self.context.get_type(str(node.id))

        if self.current_type.parent:
            parent_type = self.current_type.parent
            if type(parent_type) == ErrorType():
                self.errors.append(errors(node.line, 0, f'Invalid parent type for protocol "{node.id}"', "SEMANTIC ERROR"))

        for method in node.methods:
            self.visit(method)

        self.current_type = None

    @visitor.when(FunctionDeclNode)
    def visit(self, node):
        if node.id.startswith('<error>'):
            return

        if self.current_type != None:
            method = self.current_type.get_method(node.id)
        else:
            method = self.context.get_type("Function").get_method(node.id)

        # scope = scope.create_child()

        if node.args and method.param_types:
            for param, param_type in zip(node.args, method.param_types):
                node.scope.parent.define_variable(param.id, param_type)

        return_type = self.visit(node.body)
        if node.body and not return_type.conforms_to(method.return_type) and method.return_type != self.object_type:
            self.errors.append(errors(node.line, 0, 'Incompatible return type', "SEMANTIC ERROR"))

    def prototipes(self, clas, prot):
        if not all(method in prot.methods for method in clas.methods):
            return False
        if not all(att in prot.attributes for att in clas.attributes):
            return False
        return True

    @visitor.when(VariableDeclNode)
    def visit(self, node):
        if node.id.startswith('<error>'):
            return

        if node.id == "self":
            return self.object_type

        if node.type != None:
            try:
                var_type = self.context.get_type(str(node.type))
            except SemanticError as e:
                self.errors.append(errors(node.line, 0, e.text, "SEMANTIC ERROR"))
                var_type = ErrorType()
        else:
            var_type = self.object_type
        expr_type = self.visit(node.expr)

        if not expr_type.conforms_to(var_type) and not self.prototipes(expr_type, var_type):
            self.errors.append(errors(node.line, 0, f'Incompatible variable type, variable "{node.id}" with type "{expr_type}"', "SEMANTIC ERROR"))
        var_type = expr_type
        
        aux = node.scope.find_variable(node.id)
        if aux == None or aux.type.name == 'None':
            node.scope.replace_variable(node.id, var_type, aux)
        else:
            node.scope.parent.define_variable(node.id, var_type)

    @visitor.when(ExpBlockNode)
    def visit(self, node):
        expr_type = ErrorType()
        for expr in node.expLineList:
            expr_type = self.visit(expr)
        return expr_type

    @visitor.when(FunctCallNode)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]
        try:
            function = self.context.get_type('Function').get_method(node.lex)
        except SemanticError as e:
            self.errors.append(errors(node.line, 0, str(e), "SEMANTIC ERROR"))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        if len(args_types) != len(function.param_types):
            self.errors.append(errors(node.line, 0, f'Expected {len(function.param_types)} arguments but got {len(args_types)}', "SEMANTIC ERROR"))
            return ErrorType()

        for arg_type, param_type in zip(args_types, function.param_types):
            if arg_type.name != 'None' and param_type.name != 'None' and not arg_type.conforms_to(param_type):
                self.errors.append(errors(node.line, 0, f'Incompatible argument type {arg_type} for parameter type {param_type}', "SEMANTIC ERROR"))
                return ErrorType()

        return function.return_type

    @visitor.when(AttributeCallNode)
    def visit(self, node):
        obj_type = self.visit(node.lex)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            attr = obj_type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(errors(node.line, 0, str(e), "SEMANTIC ERROR"))
            return ErrorType()

    @visitor.when(IfExpNode)
    def visit(self, node):
        types = []
        cond_type = self.visit(node.cond)
        if_type = self.visit(node.if_expr)
        elif_type = self.visit(node.elif_expr)
        else_type = self.visit(node.else_expr)
        if cond_type != self.context.get_type('Boolean'):
            self.errors.append(errors(node.line, 0, 'Condition must be of type bool', "SEMANTIC ERROR"))
        if if_type == ErrorType():
            types.append(if_type)
        if elif_type == ErrorType():
            types.append(elif_type)
        if else_type == ErrorType():
            types.append(else_type)
        if len(types) == 0:
            return self.object_type
        return types[0] if len(types) == 1 else self.context.lowest_common_ancestor(types)

    @visitor.when(WhileExpNode)
    def visit(self, node):
        cond_type = self.visit(node.cond)
        if cond_type != self.context.get_type('Boolean'):
            self.errors.append(errors(node.line, 0, 'Condition must be of type bool', "SEMANTIC ERROR"))
        return self.visit(node.expr)

    @visitor.when(ForExpNode)
    def visit(self, node):
        iterable_type = self.visit(node.expr)
        iterable_protocol = self.context.get_type('Iterable')
        if not iterable_type.conforms_to(iterable_protocol):
            self.errors.append(errors(node.line, 0, 'Expression must conform to Iterable protocol', "SEMANTIC ERROR"))
        try:
            vtype = self.context.get_type(node.id)
        except Exception as e:
            try:
                vtype = iterable_type.methods[1].return_type
            except:
                vtype = self.object_type

        node.scope.parent.define_variable(node.id, vtype)
        return self.visit(node.body)

    @visitor.when(LetExpNode)
    def visit(self, node):
        # scope = scope.create_child()
        for varAssignation in node.varAssignation:
            self.visit(varAssignation)
        return self.visit(node.expr)

    @visitor.when(NewExpNode)
    def visit(self, node):
        try:
            ttype = self.context.get_type(str(node.id))
            args_types = [self.visit(arg) for arg in node.args]
        except SemanticError as e:
            return ErrorType()

        if len(args_types) != len(ttype.attributes):
            self.errors.append(errors(node.line, 0, f'Expected {len(ttype.attributes)} arguments but got {len(args_types)} calling "{node.id}"', "SEMANTIC ERROR"))
            return ErrorType()

        for arg_type, attr in zip(args_types, ttype.attributes):
            try:
                param_type = self.context.get_type(str(attr))
                if not arg_type.conforms_to(param_type):
                    self.errors.append(errors(node.line, 0, f'Incompatible argument type {arg_type} for parameter type {param_type} while calling "{node.id}"', "SEMANTIC ERROR"))
                    return ErrorType()
            except Exception as e:
                return ErrorType()
        return ttype

    @visitor.when(VariableNode)
    def visit(self, node):
        if node.lex == "self":
            return self.object_type
        var = node.scope.find_variable(str(node.lex))
        if var is None:
            self.errors.append(errors(node.line, 0, f'Variable {node.lex} not defined', "SEMANTIC ERROR"))
            return ErrorType()

        return var.type

    # region base_types
    @visitor.when(NumberNode)
    def visit(self, node):
        return self.context.get_type('Number')

    @visitor.when(BooleanNode)
    def visit(self, node):
        return self.context.get_type('Boolean')

    @visitor.when(StringNode)
    def visit(self, node):
        return self.context.get_type('String')

    # region aritm_ops

    @visitor.when(PlusNode)
    def visit(self, node:Node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
            left_type = number_type
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)
            right_type = number_type

        
        

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return number_type

    @visitor.when(MinusNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(MultiplicationNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(DivisionNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(ModuleNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(PowerNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type in [None, 'None'] or left_type.name in [None, 'None']:
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type in [None, 'None'] or right_type.name in [None, 'None']:
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Number')

    # region comparison
    @visitor.when(LessThanNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(LessThanEqualNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(EqualNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(NotEqualNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        number_type = self.context.get_type('Number')
        
        if left_type.name == None or left_type.name == 'None':
            aux = node.scope.find_variable(node.left.lex)
            node.scope.replace_variable(node.left.lex, number_type, aux)
        if right_type.name == None or right_type.name == 'None':
            aux = node.scope.find_variable(node.right.lex)
            node.scope.replace_variable(node.right.lex, number_type, aux)

        left_type = number_type
        right_type = number_type

        accepted = [number_type, AutoType()]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(errors(node.line, 0, f'Invalid comparison between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(AndNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != self.context.get_type('Boolean') or right_type != self.context.get_type('Boolean'):
            self.errors.append(errors(node.line, 0, f'Invalid logical operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(OrNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != self.context.get_type('Boolean') or right_type != self.context.get_type('Boolean'):
            self.errors.append(errors(node.line, 0, f'Invalid logical operation between {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(NotNode)
    def visit(self, node):
        expr_type = self.visit(node.node) #! node.node o node.value??

        if expr_type != self.context.get_type('Boolean'):
            self.errors.append(errors(node.line, 0, f'Invalid logical operation with {expr_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node):
        expr_type = self.visit(node.left)
        cast_type = self.context.get_type(str(node.right))

        if not expr_type.conforms_to(cast_type) and not cast_type.conforms_to(expr_type):
            self.errors.append(errors(node.line, 0, f'Cannot cast {expr_type} to {cast_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return cast_type

    @visitor.when(IsNode)
    def visit(self, node):
        self.visit(node.left)
        self.context.get_type(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(IndexExpNode)
    def visit(self, node):
        index_type = self.visit(node.expr)
        if index_type != self.context.get_type('Number'):
            self.errors.append(errors(node.line, 0, f'Index must be of type int, not {index_type}', "SEMANTIC ERROR"))
            return ErrorType()

        obj_type = self.visit(node.factor)
        if not isinstance(obj_type, VectorType):
            self.errors.append(errors(node.line, 0, f'Cannot index into non-vector type {obj_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return obj_type.get_element_type()

    @visitor.when(VectorNode)
    def visit(self, node):
        elements_types = [self.visit(element) for element in node.lex]
        lca = self.context.lowest_common_ancestor(elements_types)
        if lca != ErrorType():
            return ErrorType()
        vtype = VectorType(lca, self.context.get_type('Iterable'))
        return vtype

    @visitor.when(VectorIterableNode)
    def visit(self, node):
        iterable_type = self.visit(node.iterable) 
        iterable_protocol = self.context.get_type('Iterable')
        if not iterable_type.conforms_to(iterable_protocol):
            self.errors.append(errors(node.line, 0, f'{iterable_type} does not conform to Iterable protocol', "SEMANTIC ERROR"))
            return ErrorType()

        # scope = scope.create_child()
        node.scope.parent.define_variable(node.id, iterable_type)

        return_type = self.visit(node.expr)
        if return_type != ErrorType():
            return ErrorType()

        return VectorType(return_type, self.context.get_type('Iterable'))

    @visitor.when(ConcatNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        concatenable = [self.context.get_type('String'), self.context.get_type('Number'), self.context.get_type('Object')]
        if left_type not in concatenable or right_type not in concatenable:

            self.errors.append(errors(node.line, 0, f'Invalid concatenation between types {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('String')

    @visitor.when(ConcatSpaceNode)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        concatenable = [self.context.get_type('String'), self.context.get_type('Number'), self.context.get_type('Object')]
        if left_type not in concatenable or right_type not in concatenable:

            self.errors.append(errors(node.line, 0, f'Invalid concatenation between types {left_type} and {right_type}', "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type('String')

    @visitor.when(PropertyCallNode)
    def visit(self, node):
        obj_type = self.visit(node.lex)

        if obj_type != ErrorType():
            return ErrorType()

        try:
            method = obj_type.get_method(node.id)
            return method.return_type
        except SemanticError as e:
            self.errors.append(errors(node.line, 0, str(e), "SEMANTIC ERROR"))
            return ErrorType()

    @visitor.when(AssignExpNode)
    def visit(self, node):
        try:
            var_info = node.scope.find_variable(node.var.id)
        except AttributeError:
            var_info = node.scope.find_variable(node.var.lex)
        if var_info is None:
            try:
                self.errors.append(errors(node.line, 0, f'Variable "{node.var.id}" not defined on scope', "SEMANTIC ERROR"))
                return ErrorType()
            except AttributeError:
                self.errors.append(errors(node.line, 0, f'Variable "{node.var.lex}" not defined on scope', "SEMANTIC ERROR"))
                return ErrorType()

        expr_type = self.visit(node.expr)
        if not expr_type.conforms_to(var_info.type):
            self.errors.append(errors(node.line, 0, f'Cannot assign "{expr_type}" to "{var_info.type}"', "SEMANTIC ERROR"))
            return ErrorType()

        return var_info.type
