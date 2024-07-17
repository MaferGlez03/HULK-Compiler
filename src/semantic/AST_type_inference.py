from cmp.visitor import *
from cmp.semantic import *
from cmp.semantic import *
from grammar.H_ast import *
from Tools.Errors import *


class type_inference:
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.current_type = None
        self.current_func = None
        self.object_type = self.context.get_type("Object")
        self.errors = errors
        self.it = 0

    @visitor.on('node')
    def visit(self, node):
        self.Errors

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for definition in node.definitionList:
            self.visit(definition)
        self.visit(node.globalExpression)
        return self.context, self.errors

    @visitor.when(ExpBlockNode)
    def visit(self, node: ExpBlockNode):
        expr_type = ErrorType()
        for item in node.expLineList:
            expr_type = self.visit(item)
        return expr_type
    # region Binary Expressions

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(DivisionNode)
    def visit(self, node: DivisionNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(MultiplicationNode)
    def visit(self, node: MultiplicationNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(ModuleNode)
    def visit(self, node: ModuleNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(PowerNode)
    def visit(self, node: PowerNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('String')

    @visitor.when(ConcatSpaceNode)
    def visit(self, node: ConcatSpaceNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('String')

    @visitor.when(AndNode)
    def visit(self, node: AndNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(OrNode)
    def visit(self, node: OrNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        self.visit(node.left)
        self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        self.visit(node.left)
        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        self.visit(node.left)
        as_type = self.context.get_type(str(node.right))
        return as_type
    # end region

    # region Unary Expressions
    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        self.visit(node.node)
        return self.context.get_type('Boolean')

    @visitor.when(NegNode)
    def visit(self, node: NegNode):
        self.visit(node.node)
        return self.context.get_type('Number')
    # end region

    # region Atoms

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        types = [self.visit(item) for item in node.lex]
        lca = self.context.lowest_common_ancestor(types)
        if type(lca) != ErrorType():
            vector_type = VectorType(lca, self.context.get_type('Iterable'))
            return vector_type
        return ErrorType()

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode):
        if node.lex == "self":
            return self.current_type
        try:
            var = node.scope.find_variable(node.lex)
        except SemanticError as error:
            self.errors.append(Errors(node.line, -1, str(error), 'Semantic Error'))
            return ErrorType()
        return var.type

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode):
        return self.context.get_type('Number')

    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        return self.context.get_type('String')

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode):
        return self.context.get_type('Boolean')

    @visitor.when(NewExpNode)
    def visit(self, node: NewExpNode):
        try:
            new_type = self.context.get_type(node.id)
            args_types = [self.visit(arg) for arg in node.args]
        except SemanticError as e:
            return ErrorType()
        attr = new_type.attributes
        attr_ = [attri for attri in attr if (attri.name.startswith('IN') and attri.name.endswith('ESP'))]
        if len(args_types) != len(attr_) and len(args_types) != 0:
            self.errors.append(Errors(node.line, -1, f'New: Type {node.id} expects {len(attr)} but {len(args_types)} were given', 'Semantic Error'))
            return ErrorType()
        return new_type

    @visitor.when(AssignExpNode)
    def visit(self, node: AssignExpNode):
        try:
            variable = node.var.id
        except:
            variable = node.var.lex
        if variable == "self":
            self.errors.append(Errors(node.line, -1, "You can't modify self", 'Semantic Error'))
            return self.current_type
        var = node.scope.find_variable(variable)
        if var is not None:
            type = self.visit(node.expr)
            if var.type.name != AutoType().name:
                return var.type
            node.scope.replace_variable(variable, type)
            return type
        self.errors.append(Errors(node.line, -1, f'Variable {variable} is not defined', 'Semantic Error'))

    @visitor.when(LetExpNode)
    def visit(self, node: LetExpNode):
        for item in node.varAssignation:
            self.visit(item)
            type_ = self.visit(node.expr)
        return type_

    @visitor.when(WhileExpNode)
    def visit(self, node: WhileExpNode):
        self.visit(node.cond)
        type_ = self.visit(node.expr)
        return type_

    @visitor.when(ForExpNode)
    def visit(self, node: ForExpNode):
        self.visit(node.expr)
        try:
            var = self.context.get_type(str(node.id))
        except Exception:
            var = AutoType()
            type_ = self.visit(node.body)
        return type_

    @visitor.when(IfExpNode)
    def visit(self, node: IfExpNode):
        types = []
        self.visit(node.cond)
        if_type = self.visit(node.if_expr)
        elif_type = self.visit(node.elif_expr)
        else_type = self.visit(node.else_expr)
        if type(if_type) != ErrorType() and if_type != []:
            types.append(if_type)
        if type(elif_type) != ErrorType() and elif_type != []:
            types.append(elif_type)
        if type(else_type) != ErrorType() and else_type != []:
            types.append(else_type)
        if len(types) == 0:
            return AutoType()
        if len(types) == 1:
            return types[0]
        else:
            type_ = self.context.lowest_common_ancestor(types)
            return type_

    @visitor.when(IndexExpNode)
    def visit(self, node: IndexExpNode):
        self.visit(node.expr)
        type_ = self.visit(node.factor)
        if not isinstance(type_, VectorType):
            return ErrorType()
        return type_.get_element_type()

    @visitor.when(VectorIterableNode)
    def visit(self, node: VectorIterableNode):
        iterable = self.visit(node.iterable)
        if not iterable.conforms_to(self.context.get_type('Iterable')):
            self.errors.append(Errors(node.line), 0, f'{iterable} is not an iterable object')
            return ErrorType()
        type_ = self.visit(node.expr)
        return VectorType(type_, self.context.get_type('Iterable')) if type_ != ErrorType() else ErrorType()

    @visitor.when(ProtocolDeclNode)
    def visit(self, node: ProtocolDeclNode):
        self.current_type = self.context.get_type(str(node.id))
        if self.current_type.parent:
            parent = self.current_type.parent
            if type(parent) == ErrorType():
                self.errors.append(Errors(node.line, -1, f'Invalid parent type for {node.id} protocol'))

        for item in node.methods:
            self.visit(item)
        self.current_type = None

    @visitor.when(FunctionDeclNode)
    def visit(self, node: FunctionDeclNode):
        self.current_func = node.id
        if node.id.startswith('<error>'):
            return node.return_type
        if self.current_type != None:
            method = self.current_type.get_method(node.id)
        else:
            method = self.context.get_type("Function").get_method(node.id)

        body_type = self.visit(node.body)
        if node.return_type != None and node.return_type != AutoType().name:
            node.scope.return_type = self.context.get_type(str(node.return_type))
        else:
            node.scope.return_type = body_type
            method.return_type = body_type

        self.current_function = None

    @visitor.when(VariableDeclNode)
    def visit(self, node: VariableDeclNode):
        if node.id.startswith('<error>'):
            return

        if node.id == "self":
            return self.current_type

        if node.type != None:
            try:
                var_type = self.context.get_type(str(node.type))
            except SemanticError as e:
                var_type = ErrorType()
        else:
            var_type = AutoType()
        expr_type = self.visit(node.expr)
        if var_type.name == AutoType().name:
            var_type = expr_type
            node.scope.replace_variable(node.id, expr_type)

    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        _type = self.visit(node.lex)

        try:
            attr = _type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(Errors(node.line, -1, str(e), "Semantic Error"))
            return ErrorType()

    @visitor.when(PropertyCallNode)
    def visit(self, node: PropertyCallNode):

        variable = node.lex
        _type = self.visit(variable)

        if _type == ErrorType():
            return ErrorType()
        try:
            method = _type.get_method(node.id)
            return method.return_type
        except SemanticError as e:
            if _type != AutoType():
                self.errors.append(Errors(node.line, -1, str(e), "Semantic Error"))
            return AutoType()

    @visitor.when(FunctCallNode)
    def visit(self, node: FunctCallNode):
        args_types = [self.visit(arg) for arg in node.args]
        fun_name = node.lex
        curr = 'Function'
        # if self.current_type!=None:
        #     curr=self.current_type.name
        if node.lex == "base":
            curr = self.current_type.parent.name
            fun_name = self.current_func
        try:
            function = self.context.get_type(str(curr)).get_method(fun_name)
        except SemanticError as e:
            self.errors.append(Errors(node.line, -1, str(e), "Semantic Error"))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()
        if len(args_types) != len(function.param_types):
            self.errors.append(Errors(node.line, -1, f'Function: Expected {len(function.param_types)} arguments but got {len(args_types)}', "Semantic Error"))
            return ErrorType()

        return function.return_type

    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode):
        if node.id.startswith('<error>'):
            return

        self.current_type = self.context.get_type(node.id)

        if self.it == 0:
            if len(node.args) == 0 and node.parents != None:
                try:
                    params = self.context.get_type(str(node.parents)).attributes
                except SemanticError as e:
                    self.errors.append(Errors(node.line, -1, f'Invalid parent type for "{node.id}"', "Semantic Error"))
                    return ErrorType()

                for param in params:
                    node.args.append(VariableDeclNode(param.name, param.type.name if param.type != AutoType() else None, None))
                    node.args.append(VariableNode(param.name))
                    try:
                        node.scope.locals.append(param)
                        self.current_type.define_attribute('IN'+param.name+'ESP', node.scope.find_variable(param.name).type)
                    except SemanticError as e:
                        self.current_type.define_attribute('IN'+param.name+'ESP', AutoType())
            else:
                for param in node.args:
                    add = True
                    if param.id in [at.name for at in self.current_type.attributes]:
                        add = False
                    try:
                        self.current_type.define_attribute('IN'+param.id+'ESP', node.scope.find_variable(param.id).type)
                    except SemanticError as e:
                        if add:
                            self.current_type.define_attribute('IN'+param.id+'ESP', AutoType())

        if self.current_type.parent:
            if type(self.current_type.parent) == ErrorType():
                self.errors.append(Errors(node.line, -1, f'Invalid parent type for "{node.id}"', "Semantic Error"))

        for attr in node.attributes:
            self.visit(attr)
        self.current_type = None
