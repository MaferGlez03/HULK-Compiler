from cmp.visitor import *
from cmp.semantic import *
from cmp.semantic import *
from grammar.H_ast import *
from Tools.Errors import *
from typing import List


class type_inference:
    def __init__(self, context: Context, errors: Errors = []):
        self.context: Context = context
        self.current_type: Type = None
        self.current_function: Function = None
        self.object_type = self.context.get_type("Object")
        self.errors: List[Errors] = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for definition in node.definitionList:
            self.visit(definition)
        self.visit(node.globalExpression)
        return self.context, self.errors

    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode):
        if node.id.startswith('<error>'):
            return
        self.current_type = self.context.get_type(node.id)
        for declaration in node.attributes:
            self.visit(declaration)
        self.current_type = None

    @visitor.when(ProtocolDeclNode)
    def visit(self, node: ProtocolDeclNode):
        if node.id.startswith('<error>'):
            return
        self.current_type = self.context.get_type(node.id)
        for method in node.methods:
            self.visit(method)
        self.current_type = None

    def protocol_coincidence(self, protocol_type: Type, assign_type: Type):
        if all(prot_method.name in [method.name for method in assign_type.methods] for prot_method in protocol_type.methods):
            return True
        return False

    @visitor.when(FunctionDeclNode)
    def visit(self, node: FunctionDeclNode):
        if node.id.startswith('<error>'):
            return
        self.current_function = node.id

        # * None means not declareted
        if node.return_type == None:
            return_type = AutoType()
        else:
            return_type = self.context.get_type(node.return_type)
        arg_names = []
        arg_types = []
        for arg in node.args:
            arg_names.append(arg.id)
            if arg.type == None:
                arg.type = AutoType().name  # ! |||||||| LO ARREGLA LA INFERENCIA DE TIPO ||||||||||||||||||
                arg_types.append(arg.type)
            else:
                arg_types.append(arg.type)
            node.scope.define_variable(arg.id, arg.type)

        # * Check types into body works
        if node.body == None:
            body_type = AutoType()
        else:
            body_type = self.visit(node.body)

        if not body_type.conforms_to(return_type):
            self.errors.append(Errors(node.line, -1, f"Function \"{node.id}\" body type \"{body_type}\" not conforms to function return type \"{return_type}\"", "SEMANTIC ERROR"))

        self.current_function = None

    @visitor.when(VariableDeclNode)
    def visit(self, node: VariableDeclNode):
        if node.id.startswith('<error>'):
            return
        if node.id == "self":
            return self.current_type

        if node.type != None:
            try:
                var_type = self.context.get_type(node.type)
            except SemanticError as e:
                self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
                var_type = ErrorType()
        else:
            var_type = AutoType()
        expr_type = self.visit(node.expr)

        if var_type.name == AutoType().name:
            node.scope.replace_variable(node.id, expr_type)
            var_type = expr_type

        if not expr_type.conforms_to(var_type) and not self.protocol_coincidence(var_type, expr_type):
            self.errors.append(Errors(node.line, -1, f'Incompatible variable type, variable "{node.id}" with type "{expr_type}"', "SEMANTIC ERROR"))
        var_type = expr_type

    @visitor.when(ExpBlockNode)
    def visit(self, node: ExpBlockNode):
        expr_type = ErrorType()
        for expression in node.expLineList:
            expr_type = self.visit(expression)
        return expr_type

    @visitor.when(NewExpNode)
    def visit(self, node: NewExpNode):
        try:
            return_type = self.context.get_type(node.id)
        except SemanticError as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()

        try:
            args_types = [self.visit(arg) for arg in node.args]
        except SemanticError as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()

        attributes = []
        if len(args_types) != len(return_type.attributes):
            if len(args_types) == len(return_type.parent.attributes):
                attributes = return_type.parent.attributes
            elif len(args_types) == 0:
                return return_type
            else:
                self.errors.append(Errors(node.line, -1, f'Expected {len(return_type.attributes)} arguments but got {len(args_types)} calling "{node.id}"', "SEMANTIC ERROR"))
                return ErrorType()
        else:
            attributes = return_type.attributes

        for arg_type, attribute in zip(args_types, attributes):
            try:
                param_type = self.context.get_type(attribute.type.name)
                if not arg_type.conforms_to(param_type):
                    self.errors.append(Errors(node.line, -1, f'Incompatible argument type "{arg_type.name}" for parameter type "{param_type.name}" while calling "{node.id}"', "SEMANTIC ERROR",))
                    return ErrorType()
            except Exception as e:
                return ErrorType()
        return return_type

    @visitor.when(AssignExpNode)
    def visit(self, node: AssignExpNode):
        var_type = self.visit(node.var)
        # if var_type is None:
        #     self.errors.append(Errors(node.line, -1, f"Variable {node.var} not defined on program", "SEMANTIC ERROR"))
        #     return ErrorType()
        expr_type = self.visit(node.expr)
        if expr_type.conforms_to(var_type):
            var_type.type = expr_type
            return expr_type
        else:
            self.errors.append(Errors(node.line, -1, f'Cannot assign "{expr_type}" to "{var_type.type}"', "SEMANTIC ERROR"))
            return ErrorType()

    @visitor.when(LetExpNode)
    def visit(self, node: LetExpNode):
        for assign in node.varAssignation:
            self.visit(assign)
        return self.visit(node.expr)

    @visitor.when(WhileExpNode)
    def visit(self, node: WhileExpNode):
        cond_type = self.visit(node.cond)
        if cond_type != self.context.get_type("Boolean"):
            self.errors.append(Errors(node.line, -1, f"Condition type must be Boolean not {cond_type}", "SEMANTIC ERROR"))
        return self.visit(node.expr)

    @visitor.when(ForExpNode)
    def visit(self, node: ForExpNode):
        try:
            var = node.scope.find_variable(node.id)
        except Exception as e:
            self.errors.append(Errors(node.line, 0, str(e), "SEMANTIC ERROR"))
            return ErrorType()
        try:
            iterable_type = self.context.get_type(str(var.type))
        except:
            self.errors.append(Errors(node.line, -1, "You must be assign an iterable", "SEMANTIC ERROR"))
            return ErrorType()
        expr_type = self.visit(node.expr)

        try:
            if not expr_type.element_type.conforms_to(iterable_type):
                self.errors.append(Errors(node.line, -1, f'Expression type must be conforms to Iterable protocol', "SEMANTIC ERROR"))
        except:
            if not expr_type.conforms_to(iterable_type):
                self.errors.append(Errors(node.line, -1, f'Expression type must be conforms to Iterable protocol', "SEMANTIC ERROR"))

        # ? var = node.scope.find_variable(node.id)
        # ? if var is None:
        # ?     self.errors.append(Errors(node.line, -1, f'Variable {node.id} not defined on program', "SEMANTIC ERROR"))
        # ? else:
        # ?     try:
        # ?         self.context.get_type(var.type)
        # ?     except Exception as e:
        # ?         self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))

        return self.visit(node.body)

    @visitor.when(IfExpNode)
    def visit(self, node: IfExpNode):
        cond_type = self.visit(node.cond)
        if cond_type != self.context.get_type("Boolean"):
            self.errors.append(Errors(node.line, -1, f"Condition type must be Boolean not {cond_type}", "SEMANTIC ERROR"))
            return ErrorType()
        types = []
        num_autotypes = 0
        if_type = self.visit(node.if_expr)
        if not if_type.name == AutoType().name:
            types.append(if_type)
        else:
            num_autotypes += 1
        if not node.elif_expr is None:
            for elif_expr in node.elif_expr:
                elif_type = self.visit(elif_expr)
                if not elif_type.name == AutoType().name:
                    types.append(elif_type)
                else:
                    num_autotypes += 1
        if not node.else_expr is None:
            types.append(self.visit(node.else_expr))
        if len(types) + num_autotypes == 0 or (len(types) + num_autotypes == 1 and not node.else_expr is None):
            self.errors.append(Errors(node.line, -1, "You must be define body to all branches", "SEMANTIC ERROR"))
            return ErrorType()
        else:
            return types[0] if len(types) == 1 else self.context.lowest_common_ancestor(types)

    @visitor.when(IndexExpNode)
    def visit(self, node: IndexExpNode):
        # * Check index type us number
        index_type = self.visit(node.expr)
        number_type = self.context.get_type("Number")
        if not index_type.conforms_to(number_type):
            self.errors.append(Errors(node.line, -1, f"Index must be of type int, not {index_type}", "SEMANTIC ERROR"))

        # * Check vector type is iterable
        vector_type = self.visit(node.factor)
        iterable_type = self.context.get_type("Iterable")
        if not vector_type.conforms_to(iterable_type):
            self.errors.append(Errors(node.line, -1, f"Cannot index on a {vector_type}, it's not iterable", "SEMANTIC ERROR"))

        try:
            return vector_type.element_type
        except:
            return ErrorType()

    @visitor.when(VectorIterableNode)
    def visit(self, node: VectorIterableNode):
        variable = node.scope.find_variable(node.id)
        iterable_type = self.visit(node.iterable)
        try:
            if not iterable_type.element_type.conforms_to(variable.type):
                self.errors.append(Errors(node.line, -1, f"Expression element type must be conforms to {variable.type}", "SEMANTIC ERROR"))
                return ErrorType()
        except:
            if not iterable_type.conforms_to(variable.type):
                self.errors.append(Errors(node.line, -1, f"Expression element type must be conforms to {variable.type}", "SEMANTIC ERROR"))
                return ErrorType()
        try:
            return_type = self.visit(node.expr)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))

        return VectorType(return_type, self.context.get_type("Iterable"))

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        string_type = self.context.get_type("String")
        number_type = self.context.get_type("Number")
        correct_types = [string_type, number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The concatenation operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return string_type

    @visitor.when(ConcatSpaceNode)
    def visit(self, node: ConcatSpaceNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        string_type = self.context.get_type("String")
        number_type = self.context.get_type("Number")
        correct_types = [string_type, number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The concatenation operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return string_type

    @visitor.when(AndNode)
    def visit(self, node: AndNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        correct_types = [bool_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The AND operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(OrNode)
    def visit(self, node: OrNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        correct_types = [bool_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The OR operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The NOT EQUALS ( != ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The LESS THAN ( < ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The EQUALS ( == ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The GREATER THAN ( > ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The LESS THAN EQUALS ( <= ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        bool_type = self.context.get_type("Boolean")
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The GREATER THAN EQUALS ( >= ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        try:
            self.context.get_type(node.right)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()

        self.visit(node.left)
        return self.context.get_type("Boolean")

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The PLUS ( + ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The MINUS ( - ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(DivisionNode)
    def visit(self, node: DivisionNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The DIVISION ( / ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(MultiplicationNode)
    def visit(self, node: MultiplicationNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The MULTIPLICATION ( * ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(ModuleNode)
    def visit(self, node: ModuleNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The MODULE ( % ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(PowerNode)
    def visit(self, node: PowerNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not (left_type in correct_types or right_type in correct_types):
            self.errors.append(Errors(node.line, -1, f"The POWER ( ^ ) operation is not allowed between {left_type} and {right_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        try:
            type = self.context.get_type(node.right)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()
        self.visit(node.left)
        return type

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        node_type = self.visit(node.node)
        bool_type = self.context.get_type("Boolean")
        correct_types = [bool_type, AutoType(), AutoType().name]
        if not node_type in correct_types:
            self.errors.append(Errors(node.line, -1, f"The NOT ( ! ) operation is not allowed with {node_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return bool_type

    @visitor.when(NegNode)
    def visit(self, node: NegNode):
        node_type = self.visit(node.node)
        number_type = self.context.get_type("Number")
        correct_types = [number_type, AutoType(), AutoType().name]
        if not node_type in correct_types:
            self.errors.append(Errors(node.line, -1, f"The NEG ( - ) operation is not allowed with {node_type}", "SEMANTIC ERROR"))
            return ErrorType()
        return number_type

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        types = []
        for lex in node.lex:
            types.append(self.visit(lex))
        try:
            lca = self.context.lowest_common_ancestor(types)
        except ValueError as e:
            self.errors.append(Errors(node.line, -1, f"The elemets on a Vector must be same", "SEMANTIC ERROR"))
            return ErrorType()
        vector_type = VectorType(lca, self.context.get_type('Iterable'))
        return vector_type

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode):
        if node.lex == "self":
            return self.current_type
        try:
            variable = node.scope.find_variable(node.lex)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()
        if variable == None:
            self.errors.append(Errors(node.line, -1, f'Variable "{node.lex}" not defined on program', "SEMANTIC ERROR"))
            return ErrorType()
        try:
            return self.context.get_type(str(variable.type.name))
        except:
            try:
                return self.context.get_type(str(variable.type))
            except:

                try:
                    return self.context.get_type(str(variable.type.element_type.name))
                except:
                    return self.context.get_type(str(variable.type.element_type))

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode):
        return self.context.get_type("Number")

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode):
        return self.context.get_type("Boolean")

    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        return self.context.get_type("String")

    @visitor.when(FunctCallNode)
    def visit(self, node: FunctCallNode):
        # function_name = node.lex
        # curr = 'Function'
        # if node.lex == "base":
        #     curr = self.current_type.parent.name
        #     function_name = self.current_function

        # try:
        #     function = self.context.get_type(curr).get_method(function_name)
        if node.lex == "base":
            function = self.current_type.parent.get_method(self.current_function)
        else:
            try:
                function = self.context.get_function(node.lex)
            except SemanticError as e:
                self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
                for arg in node.args:
                    self.visit(arg)
                return ErrorType()

        if len(function.param_names) != len(node.args):
            self.errors.append(Errors(node.line, -1, f'Expected {len(function.param_names)} arguments but got {len(node.args)} calling "{node.lex}', "SEMANTIC ERROR"))
            return ErrorType()

        for arg, param_type in zip(node.args, function.param_types):
            arg_type = self.context.get_type(self.visit(arg).name)
            if not arg_type.conforms_to(param_type):
                self.errors.append(Errors(node.line, -1, f'The argument type does not match the declared argument type', "SEMANTIC ERROR"))
                return ErrorType()

        return function.return_type

    @visitor.when(PropertyCallNode)
    def visit(self, node: PropertyCallNode):
        try:
            calling_type = self.visit(node.lex)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        try:
            function = calling_type.get_method(node.id)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        for arg, param_type in zip(node.args, function.param_types):
            arg_type = self.visit(arg)
            if not arg_type.conforms_to(param_type):
                self.errors.append(Errors(node.line, -1, f'The argument type does not match the declared argument type', "SEMANTIC ERROR"))
                return ErrorType()

        return function.return_type

    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        if node.lex.lex == "self":
            calling_type = self.current_type
        else:
            try:
                calling_type = self.visit(node.lex)
            except Exception as e:
                self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
                return ErrorType()

        try:
            attribute = calling_type.get_attribute(node.id)
        except Exception as e:
            self.errors.append(Errors(node.line, -1, str(e), "SEMANTIC ERROR"))
            return ErrorType()

        return self.context.get_type(attribute.type.name)
