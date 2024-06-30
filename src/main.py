from Lexer.lexer import*
from grammar.grammar import *
from Parser.LR1_Parser import *


lexer = HULK_Lexer(G.EOF)
tokens = lexer.tokenize("let x > 10")
final=[]
for item in tokens:
  final.append(item.lex)
  
print(tokens)
print(final)
parser = LR1Parser(G)
derivation, operations = parser(final)
