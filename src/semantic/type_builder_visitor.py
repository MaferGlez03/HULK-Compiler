import src.cmp.visitor as visitor
from src.cmp.semantic import  ErrorType,SemanticError
from Tools.errors import *
from grammar.H_ast import *

class type_builder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors 
        
    @visitor.on('node')
    def visit(self, node):
        pass
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        for item in node.definitionList:
            self.visit(item)
        self.visit(node.globalExpression)
        return self.context, self.errors
    
    @visitor.when(VariableDeclNode)
    def visit(self, node:VariableDeclNode):
        try:
                var_type = self.context.get_type(node.type)
        except SemanticError as e:
            if node.type!= None:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                var_type = ErrorType()
                
        try:
            self.current_type.define_attribute(node.id, var_type)
        except SemanticError as e:
            if var_type!=ErrorType():
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                
    @visitor.when(TypeDeclNode)
    def visit(self, node: TypeDeclNode):
        
        try:
            self.current_type = self.context.get_type(node.id)
        except SemanticError as e:
            self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
            self.current_type = ErrorType()
            return
        
        if node.parents !=None:
            try:
                current = current_type_parent = self.context.get_type(node.parent)
               
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(errors(0,0,"Bucle inheritance",'Semantic Error'))#? set row and column
                        current_type_parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                current_type_parent = ErrorType()
            try:
                self.current_type.set_parent(current_type_parent)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
        elif node.parent == 'Number'or node.parent ==  'Bool'or node.parent ==  'String':
            self.errors.append(errors(0,0,"Not valid inheritance",'Semantic Error'))#? set row and column
        else:
            self.current_type.set_parent(self.context.get_type('Object'))
        for item in node.attributes:
         self.visit(item)
         
    @visitor.when(ProtocolDeclNode)
    def visit(self, node: ProtocolDeclNode):
        
        try:
            self.current_type = self.context.get_type(node.id)
        except SemanticError as e:
            self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
            self.current_type = ErrorType()
            return
        
        if node.parents !=None:
            try:
                current = current_type_parent = self.context.get_type(node.parent)
               
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(errors(0,0,"Bucle inheritance",'Semantic Error'))#? set row and column
                        current_type_parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                current_type_parent = ErrorType()
            try:
                self.current_type.set_parent(current_type_parent)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
        for item in node.methods:
         self.visit(item)