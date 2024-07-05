from src.semantic.AST_type_inference import *
from src.semantic.scope_def_visitor import *
from src.semantic.type_builder_visitor import *
from src.semantic.type_def_visitor import *


def semantic_check(ast):
    errors = []
    
    print("COLLECTING TYPES...")
    
    type_collector = typeDef(errors)
    context, errors = type_collector.visit(ast)

    print("BUILDING TYPES...")
    
    type_fill = type_builder(context, errors)
    context, errors = type_fill.visit(ast)

    print("BUILDING SCOPES...")
    
    var_collector = scopeDef(context, errors)
    scope = var_collector.visit(ast)

    scope.define_variable("PI", context.get_type("Number"))
    scope.define_variable("E", context.get_type("Number"))

    print("CHECKING TYPES...")
    
    type_inf = type_inferer(context, errors)
    context, errors = type_inf.visit(ast, scope)

    if errors:
        for error in errors:
            print(error)
        return False
    return True
