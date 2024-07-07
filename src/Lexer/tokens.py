from  grammar.grammar import *
from enum import Enum, auto

#region TokenType
class TokenType(Enum):
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    OPEN_SQUARE_BRACKET = auto()
    CLOSE_SQUARE_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    ARROW = auto()
    DOUBLE_BAR = auto()
    ASSIGMENT = auto()
    DEST_ASSIGMENT = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    PI = auto()
    E = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    MOD = auto()
    POWER = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    ARR = auto()
    DOUBLE_ARR = auto()

    EQ = auto()
    NEQ = auto()
    LEQ = auto()
    GEQ = auto()
    LT = auto()
    GT = auto()

    FUNCTION = auto()
    LET = auto()
    IN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    NEW = auto()
    IS = auto()
    AS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()
    TYPE = auto()
    INHERITS = auto()

    UNTERMINATED_STRING = auto()
    ESCAPED_CHAR = auto()
    SPACES = auto()

tokens_terminals = {
    TokenType.OPEN_PAREN: open_parenthesis__ ,
    TokenType.CLOSE_PAREN: closed_parenthesis__,
    TokenType.OPEN_BRACKET: open_curly_bracket__,
    TokenType.CLOSE_BRACKET: closed_curly_bracket__,
    TokenType.OPEN_SQUARE_BRACKET: open_square_braket__,
    TokenType.CLOSE_SQUARE_BRACKET: close_square_braket__,
    TokenType.COMMA: comma__,
    TokenType.DOT: dot__,
    TokenType.COLON: type_asignator__,
    TokenType.SEMICOLON: semicolon__,
    TokenType.ARROW: func_arrow__,
    TokenType.DOUBLE_BAR: bars__,
    TokenType.ASSIGMENT: inicialization__,
    TokenType.DEST_ASSIGMENT: assignation__,

    TokenType.IDENTIFIER: id__,
    TokenType.STRING: string__,
    TokenType.NUMBER: number__,
    TokenType.BOOLEAN: booleanValue__,
    TokenType.PI: number__,
    TokenType.E: number__,

    TokenType.PLUS: plus_operator__,
    TokenType.MINUS: minus_operator__,
    TokenType.STAR: multiplication__,
    TokenType.DIV: division__,
    TokenType.MOD: module_operation__,
    TokenType.POWER: exponentiation__,

    TokenType.AND: and__,
    TokenType.OR: or__,
    TokenType.NOT: not__,

    TokenType.ARR: string_operator__,
    TokenType.DOUBLE_ARR: string_operator_space__,

    TokenType.EQ: eq__,
    TokenType.NEQ: neq__,
    TokenType.LEQ: lte__,
    TokenType.GEQ: gte__,
    TokenType.LT: lt__,
    TokenType.GT: gt__,

    TokenType.FUNCTION: function__,
    TokenType.LET: let__,
    TokenType.IN: in__,
    TokenType.IF: if__,
    TokenType.ELSE: else__,
    TokenType.ELIF: elif__,
    TokenType.WHILE: while__,
    TokenType.FOR: for__,
    TokenType.NEW: new__,
    TokenType.IS: is__,
    TokenType.AS: as__,
    TokenType.PROTOCOL: protocol__,
    TokenType.EXTENDS: extends__,
    TokenType.TYPE: type__,
    TokenType.INHERITS: inherits__,
    

    TokenType.UNTERMINATED_STRING: 'UNTERMINATED_STRING',
    TokenType.ESCAPED_CHAR: 'ESCAPED_CHAR',
    TokenType.SPACES: 'SPACES',
}

#region hulk_tokens
def hulk_tokens():
    operators = [
        (TokenType.OPEN_BRACKET, "{"), (TokenType.CLOSE_BRACKET, "}"), (TokenType.SEMICOLON, ";"),
        (TokenType.OPEN_PAREN, "("), (TokenType.CLOSE_PAREN, ")"), (TokenType.ARROW, "=?>"), (TokenType.COMMA, ","),
        (TokenType.ASSIGMENT, "="), (TokenType.DEST_ASSIGMENT, ":?="),
        (TokenType.PLUS, "+"), (TokenType.MINUS, "-"), (TokenType.STAR, "*"), (TokenType.DIV, "/"),
        (TokenType.POWER, "^"), (TokenType.MOD, "%"), #(TokenType.POWER2, "**"),
        (TokenType.EQ, "=?="), (TokenType.NEQ, "!?="), (TokenType.LEQ, "<?="), (TokenType.GEQ, ">?="),
        (TokenType.LT, "<"), (TokenType.GT, ">"), (TokenType.AND, "&"), (TokenType.OR, "|"),
        (TokenType.NOT, "!"), (TokenType.ARR, "@"), (TokenType.DOUBLE_ARR, "@?@"), (TokenType.DOT, "."),
        (TokenType.COLON, ":"), (TokenType.DOUBLE_BAR, "||"), (TokenType.OPEN_SQUARE_BRACKET, "["),
        (TokenType.CLOSE_SQUARE_BRACKET, "]")]

    reserved_words = [
        (TokenType.LET, "l?e?t"), (TokenType.IN, "i?n"),
        (TokenType.IF, "i?f"), (TokenType.ELSE, "e?l?s?e"), (TokenType.ELIF, "e?l?i?f"),
        (TokenType.FUNCTION, "f?u?n?c?t?i?o?n"),
        (TokenType.WHILE, "w?h?i?l?e"), (TokenType.FOR, "f?o?r"),
        (TokenType.NEW, "n?e?w"), (TokenType.IS, "i?s"), (TokenType.AS, "a?s"),
        (TokenType.PROTOCOL, "p?r?o?t?o?c?o?l"), (TokenType.EXTENDS, "e?x?t?e?n?d?s"),
        (TokenType.TYPE, "t?y?p?e"), (TokenType.INHERITS, "i?n?h?e?r?i?t?s"), #(TokenType.BASE, "b?a?s?e"),
        (TokenType.BOOLEAN, "(t?r?u?e)|(f?a?l?s?e)"), (TokenType.PI, "P?I"), (TokenType.E, "E")]

    nonzero_digits = '|'.join(str(n) for n in range(1, 10))
    digits = '|'.join(str(n) for n in range(10))
    lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
    upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))

    #hacer automatas especiales para (, ), *, | y ? 
    string_regex = "\"?(\\?\\?\"|\\?\"| |!|#|$|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\?\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|}|~|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*?\""

    unterminated_string_regex = "\"?(\\?\\?\"| |!|#|$|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\?\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|}|~|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*"

    number_regex = '|'.join([f"({nonzero_digits})?({digits})*",
                         f"({nonzero_digits})?({digits})*?.?({digits})?({digits})*",
                         f"0?.?({digits})?({digits})*",
                         "0"])

    identifier_regex = f"(_|{upper_letters}|{lower_letters})?(_|{upper_letters}|{lower_letters}|{digits})*"

    hulk_tokens = operators + reserved_words + [
        (TokenType.NUMBER, number_regex), (TokenType.IDENTIFIER, identifier_regex),
        (TokenType.STRING, string_regex), (TokenType.UNTERMINATED_STRING, unterminated_string_regex),
        (TokenType.SPACES, " ? *"), (TokenType.ESCAPED_CHAR, "(\n)|(\t)"), 
    ]

    return hulk_tokens


special_tokens = [TokenType.CLOSE_PAREN, TokenType.OPEN_PAREN, TokenType.STAR, TokenType.OR, TokenType.DOUBLE_BAR]