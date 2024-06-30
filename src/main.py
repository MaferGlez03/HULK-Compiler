from .Lexer import regex, tokens, lexer

lexer = Lexer.lexer.HULK_Lexer()
lexer.tokenize("let x > 10")
