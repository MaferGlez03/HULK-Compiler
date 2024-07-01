from cmp.ast import *

class ProgramNode(Node):
    def __init__(self, definitionList, globalExpression):
        self.definitionList = definitionList
        self.globalExpression = globalExpression
        
class DefinitionNode(Node):
    pass

# region Declaration

class FunctionDeclNode(DefinitionNode):
    def __init__(self, id, args, body, return_type=None):
        self.id = id
        self.args = args
        self.body = body
        self.return_type = return_type
        
class ProtocolDeclNode(DefinitionNode):
    def __init__(self, id, methods, parents, return_type=None):
        self.id = id
        self.methods = methods
        self.parents = parents
        self.return_type = return_type
        
class TypeDeclNode(DefinitionNode):
    def __init__(self, id, attributes, parents, args, parent_args):
        self.id = id
        self.attributes = attributes
        self.parents = parents
        self.args = args
        self.parent_args = parent_args
        
class VariableDeclNode(DefinitionNode):
    def __init__(self, id, type, expr):
        self.id = id
        self.type = type
        self.expr = expr
    
#end region      

#region Expressions    

class ExpressionNode(Node):
    pass

class ExpBlockNode(ExpressionNode):
    def __init__(self, expLineList):
        self.expLineList = expLineList

class NewExpNode(ExpressionNode):
    def __init__(self, id, args):
        self.id = id
        self.args = args
        
class AssignExpNode(ExpressionNode):
    def __init__(self, var, expr) -> None:
        self.var = var
        self.expr = expr
        
class LetExpNode(ExpressionNode):
    def __init__(self, varAssignation, expr):
        self.varAssignation = varAssignation
        self.expr = expr
        
class WhileExpNode(ExpressionNode):
    def __init__(self, cond, expr) -> None:
        self.cond = cond
        self.expr = expr
        
class ForExpNode(ExpressionNode):
    def __init__(self, id, expr, body) -> None:
        self.id = id
        self.expr = expr
        self.body = body
        
class IfExpNode(ExpressionNode):
    def __init__(self, cond, if_expr, elif_expr, else_expr) -> None:
        self.cond = cond
        self.if_expr = if_expr
        self.elif_expr = elif_expr
        self.else_expr = else_expr
        
class IndexExpNode(ExpressionNode):
    def __init__(self, factor, expr):
        self.factor = factor
        self.expr = expr
        
class VectorIterableNode(ExpressionNode):
    def __init__(self, expr, id, iterable):
        self.expr = expr
        self.id = id
        self.iterable = iterable
        
#end region

#region Binary Expressions

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + str(rvalue)
    
class ConcatSpaceNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + " " + str(rvalue)

class AndNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue and rvalue
    
class OrNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue or rvalue
    
class NotEqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue != rvalue
    
class LessThanNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue < rvalue
    
class EqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue == rvalue
    
class GreaterThanNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue > rvalue
    
class LessThanEqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue <= rvalue
    
class GreaterThanEqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue >= rvalue
    
class IsNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue is rvalue
    
class AsNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return rvalue(lvalue)

class PlusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + rvalue
    
class MinusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue - rvalue
    
class DivisionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue / rvalue
    
class MultiplicationNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue * rvalue
    
class ModuleNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue % rvalue
    
class PowerNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue
    
#end region

#region Unary Expressions

class NotNode(UnaryNode):
    @staticmethod
    def operate(value):
        return not value

class NegNode(UnaryNode):
    @staticmethod
    def operate(value):
        return - value
    
#end region

#region Atoms

class VectorNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        
class VariableNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        
class NumberNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        
class BooleanNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        
class StringNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        
class FunctCallNode(AtomicNode):
    def __init__(self, lex, args):
        AtomicNode.__init__(self, lex)
        self.args = args
        
class PropertyCallNode(AtomicNode):
    def __init__(self, lex, id, args):
        AtomicNode.__init__(self, lex)
        self.args = args
        self.id = id
        
class AttributeCallNode(AtomicNode):
    def __init__(self, lex, id):
        AtomicNode.__init__(self, lex)
        self.id = id
    
