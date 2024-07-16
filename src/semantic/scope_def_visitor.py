from cmp.semantic import Scope, SemanticError, AutoType
import cmp.visitor as visitor
from grammar.H_ast import *
from Tools.Errors import *


class scopeDef:
    def __init__(self, context, current_Type=None, errors=[]):
        self.context = context
        self.current_type = current_Type
        self.errors = errors
        pass

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope = None):
        node.scope = scope = Scope()
        for item in node.definitionList:
            self.visit(item, scope.create_child())
        self.visit(node.globalExpression, scope.create_child())
        return scope

    @visitor.when(ExpBlockNode)
    def visit(self, node: ExpBlockNode, scope: Scope):
        expScope = node.scope = scope.create_child()
        for item in node.expLineList:
            self.visit(item, expScope.create_child())

    @visitor.when(NewExpNode)
    def visit(self, node: NewExpNode, scope: Scope):
        node.scope = scope
        for item in node.args:
            self.visit(item, scope.create_child())

    @visitor.when(AssignExpNode)
    def visit(self, node: AssignExpNode, scope: Scope):
        node.scope = scope
        self.visit(node.var, scope.create_child())
        self.visit(node.expr, scope.create_child())

    @visitor.when(LetExpNode)
    def visit(self, node: LetExpNode, scope: Scope):
        letScope = node.scope = scope.create_child()
        for item in node.varAssignation:
            self.visit(item, letScope)
        self.visit(node.expr, letScope)

    @visitor.when(WhileExpNode)
    def visit(self, node: WhileExpNode, scope: Scope):
        whileScope = node.scope = scope.create_child()
        self.visit(node.expr, whileScope.create_child())
        self.visit(node.cond, whileScope.create_child())

    @visitor.when(ForExpNode)
    def visit(self, node: ForExpNode, scope: Scope):
        forScope = node.scope = scope.create_child()
        forScope.define_variable(node.id, AutoType())
        self.visit(node.expr, forScope)
        self.visit(node.body, forScope.create_child())

    @visitor.when(IfExpNode)
    def visit(self, node: IfExpNode, scope: Scope):
        ifScope = node.scope = scope
        self.visit(node.cond, ifScope.create_child())
        self.visit(node.if_expr, ifScope.create_child())
        try:
            for elif_expr in node.elif_expr:
                self.visit(elif_expr, ifScope.create_child())
        except:
            self.visit(node.elif_expr, ifScope.create_child())
        self.visit(node.else_expr, ifScope.create_child())

    @visitor.when(IndexExpNode)
    def visit(self, node: IndexExpNode, scope: Scope):
        node.scope = scope
        self.visit(node.factor, scope.create_child())
        self.visit(node.expr, scope.create_child())

    @visitor.when(VectorIterableNode)
    def visit(self, node: VectorIterableNode, scope: Scope):
        node.scope = scope
        comprehension_scope = scope.create_child()
        scope.define_variable(node.id, AutoType())
        self.visit(node.expr, comprehension_scope)
        self.visit(node.iterable, scope.create_child())

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(ConcatSpaceNode)
    def visit(self, node: ConcatSpaceNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(DivisionNode)
    def visit(self, node: DivisionNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(MultiplicationNode)
    def visit(self, node: MultiplicationNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(ModuleNode)
    def visit(self, node: ModuleNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(PowerNode)
    def visit(self, node: PowerNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        node.scope = scope
        self.visit(node.node, scope.create_child())

    @visitor.when(NegNode)
    def visit(self, node: NegNode, scope: Scope):
        node.scope = scope
        self.visit(node.node, scope.create_child())

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode, scope: Scope):
        node.scope = scope
        for item in node.lex:
            self.visit(item, scope.create_child())

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        node.scope = scope

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope: Scope):
        node.scope = scope

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        node.scope = scope

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        node.scope = scope

    @visitor.when(FunctCallNode)
    def visit(self, node: FunctCallNode, scope: Scope):
        node.scope = scope
        for item in node.args:
            self.visit(item, scope.create_child())

    @visitor.when(PropertyCallNode)
    def visit(self, node: PropertyCallNode, scope: Scope):
        node.scope = scope
        for item in node.args:
            self.visit(item, scope.create_child())
        self.visit(node.lex, scope.create_child())

    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode, scope: Scope):
        node.scope = scope
        self.visit(node.lex, scope.create_child())
        self.visit(node.id, scope.create_child())

    @visitor.when(FunctionDeclNode)
    def visit(self, node: FunctionDeclNode, scope: Scope):
        func_scope = node.scope = scope.create_child()

        for item in node.args:
            try:
                if item.type == None:
                    raise SemanticError()
                func_scope.define_variable(item.id, self.context.get_type(str(item.type)))
            except SemanticError as error:
                if item.type != None:
                    self.errors.append(Errors(node.line, -1, str(error), 'Semantic Error'))
                else:
                    func_scope.define_variable(item.id, AutoType())
        self.visit(node.body, func_scope)

    @visitor.when(ProtocolDeclNode)
    def visit(self, node: ProtocolDeclNode, scope: Scope):
        node.scope = scope
        prot_scope = scope.create_child()
        self.current_type = self.context.get_type(str(node.id))
        for item in node.methods:
            self.visit(item, prot_scope)
        self.current_type = None

    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode, scope: Scope):
        node.scope = scope
        type_scope = scope.create_child()
        self.current_type = self.context.get_type(str(node.id))
        
        for param in node.args:
                try:
                    if param.type!=None:
                        node.scope.define_variable(param.id, self.context.get_type(str(param.type)))
                    else: raise SemanticError()
                except SemanticError as e:
                    node.scope.define_variable(param.id, AutoType())
        for item in node.attributes:
            self.visit(item, type_scope)
        self.current_type = None

    @visitor.when(VariableDeclNode)
    def visit(self, node: VariableDeclNode, scope: Scope):
        node.scope = scope
        var_scope = scope.create_child()
        try:
            var_type = self.context.get_type(str(node.type))
        except SemanticError as error:
            if node.type != None:
                # ? set row and column
                self.errors.append(Errors(node.line, -1, str(error), 'Semantic Error'))
            var_type = AutoType()
        if var_type == None:
            var_type =AutoType()
        scope.define_variable(node.id, var_type)
        self.visit(node.expr, var_scope)
