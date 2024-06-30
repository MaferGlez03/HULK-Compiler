from ..cmp.pycompiler import Grammar

G = Grammar()

# distinguished
program = G.NonTerminal('<program>', True)

# non terminals
globalExpression = G.NonTerminal('<globalExpression>')
expression = G.NonTerminal('<expression>')
arithmeticExpression = G.NonTerminal('<arithmeticExpression>')
power = G.NonTerminal('<power>')
term = G.NonTerminal('<term>')
factor = G.NonTerminal('<factor>')
neg = G.NonTerminal('<neg>')
stringExpression = G.NonTerminal('<stringExpression>')
stringExpression1 = G.NonTerminal('<stringExpression1>')
stringExpression2 = G.NonTerminal('<stringExpression2>')
stringExpression3 = G.NonTerminal('<stringExpression3>')
argumentList = G.NonTerminal('<argumentList>')
argumentList2 = G.NonTerminal('<argumentList2>')
expressionBlock = G.NonTerminal('<expressionBlock>')
conditionalExpression = G.NonTerminal('<conditionalExpression>')
condition = G.NonTerminal('<condition>')
elifStatement = G.NonTerminal('<elifStatement>')
variableAssign = G.NonTerminal('<variableAssign>')
functionDefinition = G.NonTerminal('<functionDefinition>')
idList = G.NonTerminal('<idList>')
typeDefinition = G.NonTerminal('<typeDefinition>')
attributeList = G.NonTerminal('<attributeList>')
attribute = G.NonTerminal('<attribute>')
inlineMethodList = G.NonTerminal('<inlineMethodList>')
protocolDefinition = G.NonTerminal('<protocolDefinition>')
vector = G.NonTerminal('<vector>')
atom = G.NonTerminal('<atom>')
definitionList = G.NonTerminal('<definitionList>')
definition = G.NonTerminal('<definition>')
methodDefinition = G.NonTerminal('<methodDefinition>')
expressionLineList = G.NonTerminal('<expressionLineList>')
parameterTypeList = G.NonTerminal('<parameterTypeList>')
idMultiple = G.NonTerminal('<idMultiple>')
inlineMethod = G.NonTerminal('<inlineMethod>')
parameterType = G.NonTerminal('<parameterType>')


# terminals
open_parenthesis__ = G.Terminal('(')
closed_parenthesis__ = G.Terminal(')')
open_curly_bracket__ = G.Terminal('{')
closed_curly_bracket__ = G.Terminal('}')
open_square_braket__ = G.Terminal('[')
close_square_braket__ = G.Terminal(']')

semicolon__ = G.Terminal(';')
comma__ = G.Terminal(',')
dot__ = G.Terminal('.')
type_asignator__ = G.Terminal(':')

function__ = G.Terminal('function')
while__ = G.Terminal('while')
for__ = G.Terminal('for')
let__ = G.Terminal('let')
in__ = G.Terminal('in')
is__ = G.Terminal('is')
as__ = G.Terminal('as')

id__ = G.Terminal('id')
number__ = G.Terminal('number')
string__= G.Terminal('string')
booleanValue__ = G.Terminal('bool')
new__ = G.Terminal('new')
type__ = G.Terminal('type')
protocol__ = G.Terminal('protocol')
extends__ = G.Terminal('extends')
inherits__ = G.Terminal('inherits')

assignation__ = G.Terminal(':=')
inicialization__ = G.Terminal('=')
func_arrow__ = G.Terminal('=>')

plus_operator__ = G.Terminal('+')
minus_operator__ = G.Terminal('-')
multiplication__ = G.Terminal('*')
division__ = G.Terminal('/')
exponentiation__ = G.Terminal('^')
module_operation__ = G.Terminal('%')

string_operator__ = G.Terminal('@')
string_operator_space__ = G.Terminal('@@')

if__ = G.Terminal('if')
elif__ = G.Terminal('elif')
else__ = G.Terminal('else')

and__ = G.Terminal('&')
or__ = G.Terminal('|')
bars__ = G.Terminal('||')
not__ = G.Terminal('!')

gt__ = G.Terminal('>')
lt__ = G.Terminal('<')
gte__ = G.Terminal('>=')
lte__ = G.Terminal('<=')
eq__ = G.Terminal('==')
neq__ = G.Terminal('!=')

#productions
program %= definitionList + globalExpression

definitionList %= G.Epsilon
definitionList %= definition + definitionList

definition %= functionDefinition
definition %= typeDefinition
definition %= protocolDefinition

functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + func_arrow__ + expression + semicolon__
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + expressionBlock
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + func_arrow__ + expression + semicolon__
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + expressionBlock

methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + func_arrow__ + expression + semicolon__
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + expressionBlock
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + func_arrow__ + expression + semicolon__
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + expressionBlock

idList %= G.Epsilon
idList %= idMultiple

idMultiple %= id__
idMultiple %= id__ + type_asignator__ + id__
idMultiple %= id__ + comma__ + idMultiple
idMultiple %= id__ + type_asignator__ + id__ + comma__ + idMultiple

typeDefinition %= type__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__
typeDefinition %= type__ + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__
typeDefinition %= type__ + id__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList +closed_curly_bracket__
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__
# typeDefinition %= type__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList +closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__

attributeList %= G.Epsilon
attributeList %= attribute + attributeList

attribute %= id__ + inicialization__ + expression + semicolon__
attribute %= id__ + type_asignator__ + id__ + inicialization__ + expression + semicolon__
attribute %= methodDefinition

protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__
protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__
# protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__ + semicolon__
# protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__ + semicolon__

inlineMethodList %= G.Epsilon
inlineMethodList %= inlineMethod + inlineMethodList

inlineMethod %= id__ + open_parenthesis__ + parameterTypeList + closed_parenthesis__ + type_asignator__ + id__ + semicolon__

parameterType %= G.Epsilon
parameterType %= parameterTypeList

parameterTypeList %= id__ + type_asignator__ + id__
parameterTypeList %= id__ + type_asignator__ + id__ + comma__ + parameterTypeList

globalExpression %= expression + semicolon__ 
globalExpression %= expressionBlock

expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__
# expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__ + semicolon__

expressionLineList %= expression + semicolon__ 
expressionLineList %= expression + semicolon__ + expressionLineList

expression %= stringExpression
expression %= new__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__
expression %= factor + assignation__ + expression
expression %= let__ + variableAssign + in__ + expression
expression %= while__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression
expression %= for__ + open_parenthesis__ + id__ + in__ + expression + closed_parenthesis__ + expression
expression %= if__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression + elifStatement + else__ + expression

stringExpression %= stringExpression1
stringExpression %= stringExpression1 + as__ + id__

elifStatement %= G.Epsilon
elifStatement %= elif__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression + elifStatement

variableAssign %= id__ + inicialization__ + expression
variableAssign %= id__ + type_asignator__ + id__ + inicialization__ + expression
variableAssign %= id__ + inicialization__ + expression + comma__ + variableAssign
variableAssign %= id__ + type_asignator__ + id__ + inicialization__ + expression + comma__ + variableAssign

stringExpression1 %= stringExpression2
stringExpression1 %= stringExpression1 + string_operator__ + stringExpression2
stringExpression1 %= stringExpression1 + string_operator_space__ + stringExpression2

stringExpression2 %= stringExpression3
stringExpression2 %= stringExpression2 + and__ + stringExpression3

stringExpression3 %= conditionalExpression
stringExpression3 %= stringExpression3 + or__ + conditionalExpression

conditionalExpression %= condition
conditionalExpression %= not__ + condition

condition %= arithmeticExpression
condition %= arithmeticExpression + neq__ + arithmeticExpression
condition %= arithmeticExpression + lt__ + arithmeticExpression
condition %= arithmeticExpression + eq__ + arithmeticExpression
condition %= arithmeticExpression + gt__ + arithmeticExpression
condition %= arithmeticExpression + lte__ + arithmeticExpression
condition %= arithmeticExpression + gte__ + arithmeticExpression
condition %= arithmeticExpression + is__ + id__

arithmeticExpression %= term
arithmeticExpression %= arithmeticExpression + plus_operator__ + term
arithmeticExpression %= arithmeticExpression + minus_operator__ + term

term %= neg
term %= term + division__ + neg
term %= term + module_operation__ + neg
term %= term + multiplication__ + neg

neg %= power
neg %= minus_operator__ + neg

power %= factor
power %= factor + exponentiation__ + power

factor %= atom
factor %= factor + dot__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__
factor %= factor + dot__ + id__
factor %= factor + open_square_braket__ + expression + close_square_braket__

atom %= id__
atom %= number__
atom %= booleanValue__
atom %= string__
atom %= id__ + open_parenthesis__ + argumentList + closed_parenthesis__
atom %= expressionBlock
atom %= open_parenthesis__ + expression + closed_parenthesis__
atom %= open_square_braket__ + argumentList + close_square_braket__
atom %= open_square_braket__ + expression + bars__ + id__ + in__ + expression + close_square_braket__

argumentList %= G.Epsilon
argumentList %= expression + argumentList2

argumentList2 %= G.Epsilon
argumentList2 %= comma__ + expression + argumentList2
