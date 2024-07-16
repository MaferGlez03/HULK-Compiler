import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class AutoType(Type):
    def __init__(self):
        super().__init__('AutoType')

    def bypass(self):
        # Permite que AutoType se conforme a cualquier otro tipo
        return True
    
    def __eq__(self, other):
        return isinstance(other, Type) and self.name == other.name

    def __str__(self):
        return 'type AutoType {}'

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type) and self.name == other.name

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)
    
class VectorType(Type):
    def __init__(self, element_type, iterable):
        super().__init__('Vector')
        self.element_type = element_type
        self.set_parent(iterable)

    def get_element_type(self):
        return self.element_type

    def conforms_to(self, other):
        if isinstance(other, VectorType):
            return self.element_type.conforms_to(other.element_type)
        return super().conforms_to(other)

    def __eq__(self, other):
        return isinstance(other, VectorType) and self.element_type == other.element_type

    def __str__(self):
        return f'Vector of {self.element_type.name}'

    def __repr__(self):
        return str(self)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class Context:
    def __init__(self):
        self.types = {}
        self.functions = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            attributes = []
            for type in self.types:
                for element in self.types[type].attributes:
                    attributes.append(element)
            try:
                diccionario = {str(element): element for element in attributes}
                return diccionario[name]
            except KeyError:
                raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)
    def create_function(self, name:str, param_names:"list[str]", param_types:list, return_type, current_node=None, body : list = []):
        if name in self.types:
            raise SemanticError(f'Function with the same name ({name}) already in context.')
        function = self.functions[name] = Function(name, param_names, param_types, return_type, current_node=current_node, body=body)
        return function
    
    def get_function(self, name:str,n):
        for func in self.functions:
            if self.functions[name].name== name and len(self.functions[name].param_names) == n:
                return self.functions[name]
        return None

    def lca(self, a: Type, b: Type) -> Type:
            ancestors_a = set()
            current = a
            while current is not None:
                ancestors_a.add(current)
                current = current.parent

            current = b
            while current is not None:
                if current in ancestors_a:
                    return current
                current = current.parent

            return None
        
    def lowest_common_ancestor(self, types: list[Type]) -> Type:
        if not types:
            raise ValueError("The types list must not be empty.")
        
        if len(types) == 1:
            return types[0]

        common_ancestor = types[0]
        for typex in types[1:]:
            common_ancestor = self.lca(common_ancestor, typex)
            if common_ancestor is None:
                break
        
        return common_ancestor
class Function:
    def __init__(self, name, param_names, return_type, param_types, current_node=None, body=None):
        self.name = name
        self.param_names = param_names
        self.param_types = param_types
        self.return_type = return_type
        self.body  = body
        self.current_node = current_node

    def __eq__(self, other):
        return other.name == self.name and other.return_type == self.return_type and other.param_types == self.param_types
    
class VariableInfo:
    def __init__(self, name, vtype, value=None):
        self.name = name
        self.type = vtype
        self.value = value
    def set_value(self,value=None):
            self.value = value

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info
    
    def replace_variable(self, vname, vtype, vreplace):
        var=self.find_variable(vname)
        var.type=vtype
        return var


    def find_variable(self, vname, index=None):
        # locals = self.locals if index is None else itt.islice(self.locals, index)
        locals = self.locals
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            if self.parent is not None:
                return self.parent.find_variable(vname, self.index)  
            else:
                raise SemanticError(f'Variable "{vname}" not found in scope')

    def find_variable1(self, vname, index=None):
        # locals = self.locals if index is None else itt.islice(self.locals, index)
        locals = self.locals 
        try:
            return next(x for x in locals if x.name[0] == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
