from .check_types import *
from .scope_def_visitor import *
from .type_builder_visitor import *
from .type_def_visitor import *
from Tools.Errors import *


def semantic_check(ast):
    errs = []
    
    print("COLLECTING TYPES...")
    
    type_collector = typeDef(errs)
    context, errs = type_collector.visit(ast)

    print("BUILDING TYPES...")
    
    type_fill = type_builder(context, errs)
    context, errs = type_fill.visit(ast)

    print("BUILDING SCOPES...")
    
    var_collector = scopeDef(context, errs)
    scope = var_collector.visit(ast)

    scope.define_variable("PI", context.get_type("Number"))
    scope.define_variable("E", context.get_type("Number"))

    print("CHECKING TYPES...")
    
    type_inf = type_inference(context, errs)
    context, errs = type_inf.visit(ast)

    if errs:
        for error in errs:
            Errors.printError(error)
        return False
    return True