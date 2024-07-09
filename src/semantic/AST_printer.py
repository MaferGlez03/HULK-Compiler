import cmp.visitor as visitor
from grammar.H_ast import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ProgramNode'
        definitionList = '\n'.join(self.visit(child, tabs + 1) for child in node.definitionList)
        globalExpression = self.visit(node.globalExpression, tabs + 1)
        return f'{ans}\n{definitionList}\n{globalExpression}'

    @visitor.when(FunctionDeclNode)
    def visit(self, node, tabs=0):
        if node.args != None and node.args != []:
            args = ', '.join(arg.id for arg in node.args)
        else:
            args = ""
        ans = '\t' * tabs + f'FunctionDeclNode: function {node.id}({args}) -> {node.return_type}'
        body = self.visit(node.body, tabs + 1) if node.body != None else ""
        return f'{ans}\n{body}'

    @visitor.when(ProtocolDeclNode)
    def visit(self, node, tabs=0):
        if node.parents:
            ans = '\t' * tabs + f'ProtocolDeclNode: protocol {node.id} extends {node.parents} -> {node.return_type}'
        else:
            ans = '\t' * tabs + f'ProtocolDeclNode: protocol {node.id} -> {node.return_type}'
        methods = '\n'.join(self.visit(child, tabs + 1) for child in node.methods)
        return f'{ans}\n{methods}'

    @visitor.when(TypeDeclNode)
    def visit(self, node, tabs=0):
        if node.args != None:
            args = ', '.join(arg.id for arg in node.args)
        else:
            args = ""
        if node.parents:
            aux_tabs = '\t' * (tabs + 1)
            if node.parent_args != None:
                parent_args = '\n'.join(self.visit(arg, tabs + 2) for arg in node.parent_args)
            else:
                parent_args = aux_tabs + "\t()"
            ans = '\t' * tabs + f'TypeDeclNode: type {node.id}({args}) inherits {node.parents}(<parent_args>)\n{aux_tabs}Parent args:\n{parent_args}'
        else:
            ans = '\t' * tabs + f'TypeDeclNode: type {node.id}({args})'
        attributes = '\n'.join(self.visit(child, tabs + 1) for child in node.attributes)
        return f'{ans}\n{attributes}'

    @visitor.when(VariableDeclNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'VariableDeclNode: {node.id}: {node.type}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(ExpBlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ExpressionBlockNode: '
        expressions = '\n'.join(self.visit(child, tabs + 1) for child in node.expLineList)
        return f'{ans}\n{expressions}'

    @visitor.when(NewExpNode)
    def visit(self, node, tabs=0):
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        ans = '\t' * tabs + f'NewExpNode: new {node.id} (<args>)'
        return f'{ans}\n{args}'

    @visitor.when(AssignExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'AssignExpNode:'
        assigns = self.visit(node.var, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{assigns}\n{expr}'

    @visitor.when(LetExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'LetExpNode: let <assignations> in <expresions>'
        assignations = '\n'.join(self.visit(Assignation, tabs + 1) for Assignation in node.varAssignation)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{assignations}\n{expr}'

    @visitor.when(WhileExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'WhileExpNode: while (<cond>)'
        cond = self.visit(node.cond, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{cond}\n{expr}'

    @visitor.when(ForExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ForExpNode: for ({node.id} in <assign>) <body>'
        assign = self.visit(node.expr, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{assign}\n{body}'

    @visitor.when(IfExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'IfExpNode: if (<cond>) <ifExpr> elif (<elifExpr>) else (<elseExpr>)'
        cond = self.visit(node.cond, tabs + 1)
        ifExpr = self.visit(node.if_expr, tabs + 1)
        elseExpr = self.visit(node.else_expr, tabs + 1)
        if node.elif_expr == [] or node.elif_expr == None:
            if node.else_expr == [] or node.else_expr == None:
                return f'{ans}\n{cond}\n{ifExpr}'
            return f'{ans}\n{cond}\n{ifExpr}\n{elseExpr}'
        elifExpr = '\nElif '.join(self.visit(elif_, tabs + 1) for elif_ in node.elif_expr)
        if node.else_expr == [] or node.else_expr == None:
                return f'{ans}\n{cond}\n{ifExpr}\n{elifExpr}'
        return f'{ans}\n{cond}\n{ifExpr}\n{elifExpr}\n{elseExpr}'

    @visitor.when(IndexExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'IndexExpNode: <factor>[<index>]'
        factor = self.visit(node.factor, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{factor}\n{expr}'

    @visitor.when(VectorIterableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'VectorIterableNode: [<expr> || {node.id} in <iterable>]'
        expr = self.visit(node.expr, tabs + 1)
        iter = self.visit(node.iterable, tabs + 1)
        return f'{ans}\n{expr}\n{iter}'

    @visitor.when(ConcatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ConcatNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(ConcatSpaceNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ConcatSpaceNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AndNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'AndNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(OrNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'OrNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(NotEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'NotEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'LessThanNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'EqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreaterThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'GreaterThanNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessThanEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'LessThanEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'GreaterThanEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(IsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'IsNode'
        left = self.visit(node.left, tabs + 1)
        right = node.right
        return f'{ans}\n{left} is {right}'

    @visitor.when(PlusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'PlusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'MinusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(DivisionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'DivisionNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(MultiplicationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'MultiplicationNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(ModuleNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'ModuleNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(PowerNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'PowerNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'AsNode: '
        left = self.visit(node.left, 0)
        right = node.right
        return f'{ans}{left} as {right}'

    @visitor.when(NotNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'NotNode'
        node = self.visit(node.node, tabs + 1)
        return f'{ans}\n{node}'

    @visitor.when(NegNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'NegNode'
        node = self.visit(node.node, tabs + 1)
        return f'{ans}\n{node}'

    @visitor.when(VectorNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'VectorNode'
        elements = '\n'.join(self.visit(lex, tabs + 1) for lex in node.lex)
        return f'{ans}\n{elements}'

    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'VariableNode {node.lex}'
        return f'{ans}'

    @visitor.when(NumberNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'NumberNode {node.lex}' 
        return f'{ans} '

    @visitor.when(BooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'BooleanNode {node.lex}'
        return f'{ans}'

    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'StringNode {node.lex}'
        return f'{ans}'

    @visitor.when(FunctCallNode)
    def visit(self, node, tabs=0):
        args = '\n'.join(self.visit(child, tabs + 1) for child in node.args)
        ans = '\t' * tabs + f'FunctCallNode {node.lex}(<args>)'
        return f'{ans}\n{args}'

    @visitor.when(PropertyCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'PropertyCallNode {node.lex.lex}.{node.id}(<args>)'
        args = ''.join(self.visit(child, tabs + 1) for child in node.args)
        return f'{ans}\n{args[1:]}'

    @visitor.when(AttributeCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'AttributeCallNode {node.lex.lex}.{node.id}'
        return f'{ans}'