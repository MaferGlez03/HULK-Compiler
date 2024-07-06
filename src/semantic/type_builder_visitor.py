import cmp.visitor as visitor
from cmp.semantic import  ErrorType,SemanticError
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
            var_type = self.context.get_type('Object')
                
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
        elif node.parent == 'Number'or node.parent ==  'Boolean'or node.parent ==  'String':
            self.errors.append(errors(0,0,"Not valid inheritance",'Semantic Error'))#? set row and column
        else:
            self.current_type.set_parent(self.context.get_type('Object'))
        for item in node.attributes:
         self.visit(item)
        self.current_type =None
         
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
                for method in current_type_parent.all_methods():
                    self.current_type.define_method(method[0].name,method[0].param_names,method[0].param_types,
                                                    method[0].return_type)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
        for item in node.methods:
         try:
                self.visit(item)
         except SemanticError as e:
                self.errors.append(errors(0,0,"Bucle inheritance",'Semantic Error'))#? set row and column
        self.current_type=None
         
    @visitor.when(FunctionDeclNode)
    def visit(self, node:FunctionDeclNode):
        params_names, params_types = self.get_params_names_and_types(node)

        if node.return_type is not None:
            try:
                return_type = self.context.get_type(node.return_type)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                return_type = ErrorType()
            
        else:
            return_type = self.context.get_type('Object')

        
        if self.current_type==None:
            try:
                function_type = self.context.get_type('Function')
                function_type.define_method(node.id, params_names, params_types, return_type)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
        else:
            try:
                self.current_type.define_method(node.id, params_names, params_types, return_type)
            except SemanticError as e:
                self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column

    def get_params_names_and_types(self, node):
        if not hasattr(node, 'args') or node.args is None:
            return [], []

        params_names = []
        params_types = []

        for param in node.args:
            param_name = param.id
            param_type_name = param.type
            if param_name in params_names:
                self.errors.append(errors(0,0,f'Param {param_name} is alrready declared','Semantic Error'))#? set row and column
                index = params_names.index(param_name)
                params_types[index] = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(param_type_name)
                except SemanticError as e:
                    if param_type_name!=None:
                        self.errors.append(errors(0,0,str(e),'Semantic Error'))#? set row and column
                    param_type = self.context.get_type('Object')
                params_types.append(param_type)
                params_names.append(param_name)

        return params_names, params_types