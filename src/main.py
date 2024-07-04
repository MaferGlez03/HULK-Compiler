import pickle
from Lexer.lexer import *
import os
from grammar.grammar import *
from Parser.LR1_Parser import *
from cmp.evaluation import *
from Semantic.AST_printer import *
from Tools.errors import *
from Tools.PKL_Files import *

# if os.path.isfile('.\\lexer_.pkl'):
#         print("LOADING LEXER")
#         lexer = PKL_Files.load_object(PKL_Files,'lexer_')
# else:
#         print("CREATING LEXER")
#         lexer = HULK_Lexer(G.EOF)    
#         PKL_Files.save_object(PKL_Files,lexer,'lexer_') 

# if os.path.isfile('.\\parser_.pkl'):
#         print("LOADING PARSER")
#         parser = PKL_Files.load_object(PKL_Files,'parser_')
# else:
#         print("CREATING LR1 PARSER")
#         parser=LR1Parser(G)    
#         PKL_Files.save_object(PKL_Files,parser,'parser_') 

lexer = HULK_Lexer(G.EOF) 
tokens = lexer.tokenize("5+2;")
print (tokens)
parser=LR1Parser(G)
derivation,operations= parser (tokens, get_shift_reduce=True)
#derivation.printError()
ast = evaluate_reverse_parse(derivation,operations,tokens)
formatter = FormatVisitor()
print(formatter.visit(ast))

