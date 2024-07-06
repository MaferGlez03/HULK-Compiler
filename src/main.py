import pickle
from Lexer.lexer import *
import os
from grammar.grammar import *
from Parser.LR1_Parser import *
from cmp.evaluation import *
from semantic.AST_printer import *
from Tools.errors import *
from Tools.PKL_Files import *
from semantic.semantic_check import *


file_path = "code/test.hulk"
code = ""
try:
    with open(file_path, 'rb') as file:
        code = file.read().decode('utf-8')
        code = code.replace('\r\n', '\n').replace('\r', '\n')
except FileNotFoundError:
    errors(0, 0, f"File '{file_path}' not found", "FILE NOT FOUND")


lexer = HULK_Lexer(G.EOF)

tokens = lexer.tokenize(code)
print(tokens)

parser = LR1Parser(G)
derivation, operations = parser(tokens, get_shift_reduce=True)

ast = evaluate_reverse_parse(derivation, operations, tokens)

formatter = FormatVisitor()
print(formatter.visit(ast))

semantic_check(ast)