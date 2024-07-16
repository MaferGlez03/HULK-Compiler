import cmp.visitor as visitor 
from cmp.semantic import Context, SemanticError, AutoType
from grammar.H_ast import *
from Tools.Errors import *

class typeDef:
    def __init__(self,errors=[]):
        self.context= None
        self.error = errors
        pass
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self,node:ProgramNode):
        self.context= Context()
        #region Types
        self.context.create_type('<void>')
        self.context.create_type('None')
        # self.context.create_type(AutoType().name)
        
        object = self.context.create_type('Object')
        number = self.context.create_type('Number')
        number.set_parent(object)

        boolean = self.context.create_type('Boolean')
        boolean.set_parent(object)

        string_ = self.context.create_type('String')
        string_.set_parent(object)
        
        function_ = self.context.create_type('Function')
        function_.set_parent(object)
        
        iterable_protocol = self.context.create_type('Iterable')
        iterable_protocol.set_parent(object)
        iterable_protocol.define_attribute('element_type', object)
        
        range_ = self.context.create_type('Range')
        range_.set_parent(iterable_protocol)
        range_.params_names, range_.params_types = ['min', 'max'], [number, number]
        range_.define_attribute('min', number)
        range_.define_attribute('max', number)
        range_.define_attribute('current', number)
        
        #region Methods
        string_.define_method('size', [], [], number)
        string_.define_method('next', [], [], boolean)
        string_.define_method('current', [], [], string_)
        
        object.define_method('equals', ['other'], [object], boolean)
        object.define_method('toString', [], [], string_)

        function_.define_method('print', ['value'], [object], string_)
        function_.define_method('sqrt', ['value'], [number], number)
        function_.define_method('sin', ['angle'], [number], number)
        function_.define_method('cos', ['angle'], [number], number)
        function_.define_method('exp', ['value'], [number], number)
        function_.define_method('log', ['base', 'value'], [number, number], number)
        function_.define_method('rand', [], [], number)
        function_.define_method('base', [], [], object)
        function_.define_method('parse', ['value'], [string_], number)
        function_.define_method('range', ['min', 'max'], [number, number], range_)

        self.context.create_function('print', ['value'], [object], string_)
        self.context.create_function('sqrt', ['value'], [number], number)
        self.context.create_function('sin', ['angle'], [number], number)
        self.context.create_function('cos', ['angle'], [number], number)
        self.context.create_function('exp', ['value'], [number], number)
        self.context.create_function('log', ['base', 'value'], [number, number], number)
        self.context.create_function('rand', [], [], number)
        self.context.create_function('base', [], [], object)
        self.context.create_function('parse', ['value'], [string_], number)
        self.context.create_function('range', ['min', 'max'], [number, number], range_)
        
        iterable_protocol.define_method('next', [], [], boolean)
        iterable_protocol.define_method('current', [], [], object)

        range_.define_method('next', [], [], boolean)
        range_.define_method('current', [], [], number)

        for item in node.definitionList:
            self.visit(item)
        self.visit(node.globalExpression)
        return self.context, self.error
    
    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode):
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.error.append(Errors(node.line, 0, str(e), 'Semantic Error'))

    @visitor.when(ProtocolDeclNode)
    def visit(self, node: ProtocolDeclNode):
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.error.append(Errors(node.line, 0, str(e), 'Semantic Error'))

        
        