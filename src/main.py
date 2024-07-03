from Lexer.lexer import *
import os
from grammar.grammar import *
from Parser.LR1_Parser import *
from cmp.evaluation import *
from semantic.AST_printer import *




lexer = HULK_Lexer(G.EOF)
tokens = lexer.tokenize("5+2;")
print (tokens)
parser = LR1Parser(G)
derivation, operations = parser ([token.token_type for token in tokens ], get_shift_reduce=True)
ast = evaluate_reverse_parse(derivation,operations,tokens)
formatter = FormatVisitor()
print(formatter.visit(ast))

