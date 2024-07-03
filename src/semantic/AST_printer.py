import cmp.visitor as visitor
from grammar.H_ast import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode'
        definitionList = '\n'.join(self.visit(child, tabs + 1) for child in node.definitionList)
        globalExpression = self.visit(node.globalExpression, tabs + 1)
        return f'{ans}\n{definitionList}\n{globalExpression}'
    
    @visitor.when(FunctionDeclNode)
    def visit(self, node, tabs=0):
        args = ', '.join(node.args)
        ans = '\t' * tabs + f'\\__FunctionDeclNode: function {node.id}({args}) -> {node.returnType}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(ProtocolDeclNode)
    def visit(self, node, tabs=0):
        if node.parents:
            ans = '\t' * tabs + f'\\__ProtocolDeclNode: protocol {node.id} extends {node.parents} -> {node.return_type}'
        else:
            ans = '\t' * tabs + f'\\__ProtocolDeclNode: protocol {node.id} -> {node.return_type}'
        methods = '\n'.join(self.visit(child, tabs + 1) for child in node.methods)
        return f'{ans}\n{methods}'
    
    @visitor.when(TypeDeclNode)
    def visit(self, node, tabs=0):
        args = ', '.join(node.args)
        if node.parents:
            parent_args = ', '.join(node.parent_args)
            ans = '\t' * tabs + f'\\__TypeDeclNode: type {node.id}({args}) inherits {node.parents}({parent_args})'
        else:
            ans = '\t' * tabs + f'\\__TypeDeclNode: type {node.id}({args})'
        attributes = '\n'.join(self.visit(child, tabs + 1) for child in node.attributes)
        return f'{ans}\n{attributes}'
    
    @visitor.when(VariableDeclNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VariableDeclNode: {node.id}: {node.type}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(ExpBlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExpressionBlockNode: '
        expressions = '\n'.join(self.visit(child, tabs + 1) for child in node.expLineList)
        return f'{ans}\n{expressions}'
    
    @visitor.when(NewExpNode)
    def visit(self, node, tabs=0):
        args = ', '.join(node.args)
        ans = '\t' * tabs + f'\\__NewExpNode: new {node.id} ({args})'
        return f'{ans}'
    
    @visitor.when(AssignExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignExpNode: {node.var} = '
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(LetExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetExpNode: let {node.varAssignation} in '
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(WhileExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__WhileExpNode: while ({node.cond})'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(ForExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ForExpNode: for ({node.id} in {node.expr})'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(IfExpNode)
    def visit(self, node, tabs=0):
        if(node.elif_expr):
            ans = '\t' * tabs + f'\\__IfExpNode: if ({node.cond}) elif {node.elif_expr} else {node.else_expr}'
        else:
            ans = '\t' * tabs + f'\\__IfExpNode: if ({node.cond}) else {node.else_expr}'
        return f'{ans}'
    
    @visitor.when(IndexExpNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IndexExpNode: {node.factor}[{node.expr}]'
        return f'{ans}'
    
    @visitor.when(VectorIterableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorIterableNode: [{node.expr} || {node.id} in {node.iterable}]'
        return f'{ans}'
    
    @visitor.when(ConcatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ConcatNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(ConcatSpaceNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ConcatSpaceNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(AndNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AndNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(NotEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(LessThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessThanNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__EqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(GreaterThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterThanNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(LessThanEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessThanEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(GreaterThanEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterThanEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(IsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IsNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(PlusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PlusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MinusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(DivisionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DivisionNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(MultiplicationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MultiplicationNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(ModuleNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ModuleNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(PowerNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PowerNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AsNode: {node.left} as {node.right}'
        return f'{ans}'
    
    @visitor.when(NotNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotNode'
        node = self.visit(node.node, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(NegNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NegNode'
        node = self.visit(node.node, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(VectorNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorNode'
        node = self.visit(node.lex, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VariableNode'
        node = self.visit(node.lex, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(NumberNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NumberNode'
        node = self.visit(node.lex, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(BooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BooleanNode'
        node = self.visit(node.lex, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__StringNode'
        node = self.visit(node.lex, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(FunctCallNode)
    def visit(self, node, tabs=0):
        args = '\n'.join(self.visit(child, tabs + 1) for child in node.args)
        ans = '\t' * tabs + f'\\__FunctCallNode {node.lex}({args})'
        return f'{ans}'
    
    @visitor.when(PropertyCallNode)
    def visit(self, node, tabs=0):
        args = '\n'.join(self.visit(child, tabs + 1) for child in node.args)
        ans = '\t' * tabs + f'\\__PropertyCallNode {node.lex}.{node.id}({args})'
        return f'{ans}'
    
    @visitor.when(AttributeCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AttributeCallNode {node.lex}.{node.id}'
        return f'{ans}'