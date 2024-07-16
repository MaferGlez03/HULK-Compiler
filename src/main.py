from Lexer.lexer import *
import os
from grammar.grammar import *
from Parser.LR1_Parser import *
from cmp.evaluation import *
from Semantic.AST_printer import *
from Tools.Errors import *
from Tools.PKL_Files import *
from Semantic.semantic_check import *
from AST_Interpreter.Interpreter import *

# region Code

file_path = "code/test.hulk"
code = ""
try:
    with open(file_path, 'rb') as file:
        code = file.read().decode('utf-8')
        code = code.replace('\r\n', '\n').replace('\r', '\n')
except FileNotFoundError:
    Errors(0, 0, f"File '{file_path}' not found", "FILE NOT FOUND")
    
# end region

# region Lexer

print('===========================BUILDING LEXER...===========================')
lexer = HULK_Lexer(G.EOF)

tokens = lexer.tokenize(code)
print(tokens)

# end region

# region Parser

if os.path.getsize("./action.pkl") != 0:
    print("===========================LOADING PARSING...===========================")
    action_table = {}
    goto_table = {}
    action = PKL_Files.load_object("action")
    productions = G.Productions

    for key, value in action.items():
            state, symbol = key
            action, tag = value

            if action == ShiftReduceParser.REDUCE:
                tag = list(filter(lambda x: str(x) == str(tag), productions))[0]

            action_table[state, G[str(symbol)]] = action, tag

    stored_goto = PKL_Files.load_object("goto")

    for key, value in stored_goto.items():
            state, symbol = key
            goto_table[state, G[str(symbol)]] = value
    print("===========================PARSER LOADED===========================")
    parser = LR1Parser(G, action_table, goto_table)
else:
    print("BUILDING PARSER")
    parser = LR1Parser(G)
    PKL_Files.save_object(parser.action, "action")
    PKL_Files.save_object(parser.goto, "goto")

derivation, operations = parser(tokens, get_shift_reduce=True) 
try: 
    derivation.printError()
    sys.exit()
except Exception:
    pass

# end region

# region Semantic Check

ast = evaluate_reverse_parse(derivation, operations, tokens)

formatter = FormatVisitor()
print(formatter.visit(ast))

if not semantic_check(ast):
    sys.exit()
    
# end region

# region Interpreter

# interpreter = Interpreter(ast)
# result = interpreter.visit(ast)

# end region
