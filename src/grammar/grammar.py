from cmp.pycompiler import Grammar

G = Grammar()

# distinguished
program = G.NonTerminal('<program>', True)

# non terminals
globalExpression = G.NonTerminal('<globalExpression>')
expression = G.NonTerminal('<expression>')
arithmeticExpression = G.NonTerminal('<arithmeticExpression>')
power = G.NonTerminal('<power>')
term = G.NonTerminal('<term>')
module = G.NonTerminal('<module>')
factor = G.NonTerminal('<factor>')
stringExpression = G.NonTerminal('<stringExpression>')
concatenation = G.NonTerminal('<concatenation>')
stringLiteral = G.NonTerminal('<stringLiteral>')
escapeSequence = G.NonTerminal('<escapeSequence>')
functionCall = G.NonTerminal('<functionCall>')
argumentList = G.NonTerminal('<argumentList>')
expressionBlock = G.NonTerminal('<expressionBlock>')
statmentList = G.NonTerminal('<statmentList>')
conditional = G.NonTerminal('<conditional>')
conditionalLine = G.NonTerminal('<conditionalLine>')
conditionalExpression = G.NonTerminal('<conditionalExpression>')
condition = G.NonTerminal('<condition>')
booleanValue = G.NonTerminal('<booleanValue>')
comparation = G.NonTerminal('<comparation>')
elseStatement = G.NonTerminal('<elseStatement>')
loop = G.NonTerminal('<loop>')
variableDeclaration = G.NonTerminal('<variableDeclaration>')
variableAssign = G.NonTerminal('<variableAssign>')
destructiveAssignment = G.NonTerminal('<destructiveAssignment>')
functionDefinitionList = G.NonTerminal('<functionDefinitionList>')
functionDefinition = G.NonTerminal('<functionDefinition>')
idList = G.NonTerminal('<idList>')
typeDefinition = G.NonTerminal('<typeDefinition>')
attributeList = G.NonTerminal('<attributeList>')
attribute = G.NonTerminal('<attribute>')
methodsList = G.NonTerminal('<methodsList>')
inlineMethodList = G.NonTerminal('<inlineMethodList>')
fullMethodList = G.NonTerminal('<fullMethodList>')
methodCall = G.NonTerminal('<methodCall>')
typeInstantiating = G.NonTerminal('<typeInstantiating>')
typeAtribute = G.NonTerminal('<typeAtribute>')
typeMethodCall = G.NonTerminal('<typeMethodCall>')
typeInheritance = G.NonTerminal('<typeInheritance>')
checkingType = G.NonTerminal('<checkingType>')
downcasting = G.NonTerminal('<downcasting>')
protocolDefinition = G.NonTerminal('<protocolDefinition>')
vector = G.NonTerminal('<vector>')
parameterList = G.NonTerminal('<parameterList>')
parameter = G.NonTerminal('<parameter>')
expressionLine = G.NonTerminal('<expressionLine>')
atom = G.NonTerminal('<atom>')
vectorCall = G.NonTerminal('<vectorCall>')
definitionList = G.NonTerminal('<definitionList>')
definition = G.NonTerminal('<definition>')
methodDeclaration = G.NonTerminal('<methodDeclaration>')
expressionLineList = G.NonTerminal('<expressionLineList>')

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

true__ = G.Terminal('true')
false__ = G.Terminal('false')

gt__ = G.Terminal('>')
lt__ = G.Terminal('<')
gte__ = G.Terminal('>=')
lte__ = G.Terminal('<=')
eq__ = G.Terminal('==')
neq__ = G.Terminal('!=')

#productions
program %= definitionList + globalExpression
program %= globalExpression

definitionList %= definition
definitionList %= definition + definitionList

definition %= functionDefinition
definition %= typeDefinition
definition %= protocolDefinition

functionDefinition %= function + id__ + open_parenthesis__ + idList + closed_parenthesis__ + func_arrow__ + expression
functionDefinition %= function + id__ + open_parenthesis__ + idList + closed_parenthesis__ + expressionBlock

idList %= G.Epsilon
idList %= id__
idList %= id__ + comma__ + idList
idList %= id__ + checkingType
idList %= id__ + checkingType + comma__ + idList

checkingType %= type_asignator__ + id__

typeDefinition %= type + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__
typeDefinition %= type + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__
typeDefinition %= type + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__
typeDefinition %= type + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__
typeDefinition %= type + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__ + semicolon__
typeDefinition %= type + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__ + semicolon__
typeDefinition %= type + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__ + semicolon__
typeDefinition %= type + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + methodsList + closed_curly_bracket__ + semicolon__

attributeList %= attribute + semicolon__
attributeList %= attribute + semicolon__ + attributeList

attribute %= id__ + inicialization__ + expressionLine
attribute %= id__ + checkingType + inicialization__ + expressionLine

methodsList %= G.Epsilon
methodsList %= methodDeclaration
methodsList %= methodDeclaration + methodsList

methodDeclaration %= id__ + methodCall + func_arrow__ + expressionLine
methodDeclaration %= id__ + methodCall + expressionBlock

methodCall %= open_parenthesis__ + parameterList + closed_parenthesis__

parameterList %= G.Epsilon
parameterList %= expression
parameterList %= expression + comma__ + parameterList

protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethodList + closed_curly_bracket__
protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethodList + closed_curly_bracket__
protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethodList + closed_curly_bracket__ + semicolon__
protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethodList + closed_curly_bracket__ + semicolon__

globalExpression %= expressionLine
globalExpression %= expressionBlock

expressionLine %= expression + semicolon__

expression %= stringExpression
expression %= typeInstantiating
expression %= destructiveAssignment
expression %= variableDeclaration
expression %= loop
expression %= conditional

stringExpression %= conditionalExpression
stringExpression %= conditionalExpression + downcasting
stringExpression %= stringExpression + string_operator__ + conditionalExpression
stringExpression %= stringExpression + string_operator_space__ + conditionalExpression

conditionalExpression %= condition
conditionalExpression %= condition + and__ + conditionalExpression
conditionalExpression %= condition + or__ + conditionalExpression
conditionalExpression %= not__ + condition

condition %= arithmeticExpression
condition %= arithmeticExpression + lt__ + arithmeticExpression
condition %= arithmeticExpression + gt__ + arithmeticExpression
condition %= arithmeticExpression + lte__ + arithmeticExpression
condition %= arithmeticExpression + gte__ + arithmeticExpression
condition %= arithmeticExpression + eq__ + arithmeticExpression
condition %= arithmeticExpression + neq__ + arithmeticExpression
condition %= arithmeticExpression + is__ + arithmeticExpression

arithmeticExpression %= term
arithmeticExpression %= arithmeticExpression + plus_operator__ + term
arithmeticExpression %= arithmeticExpression + minus_operator__ + term

term %= power
term %= term + multiplication__ + power
term %= term + division__ + power
term %= term + module_operation__ + power

power %= factor
power %= factor + exponentiation__ + power

factor %= atom
factor %= factor + dot__ + functionCall
factor %= factor + dot__ + methodCall
factor %= factor + vectorCall

atom %= id__
atom %= number__
atom %= booleanValue
atom %= string__
atom %= functionCall
atom %= expressionBlock
atom %= open_parenthesis__ + expression + closed_parenthesis__
atom %= vector

functionCall %= open_parenthesis__ + argumentList + closed_parenthesis__

argumentList %= expressionLine + comma__ + argumentList
argumentList %= G.Epsilon

expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__ + semicolon__
expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__

expressionLineList %= expressionLine
expressionLineList %= expressionLine + expressionLineList

conditional %= if__ + conditionalLine

conditionalLine %= open_parenthesis__ + conditionalExpression + closed_parenthesis__ + expression + elseStatement

#! Make sense??
booleanValue %= true__
booleanValue %= false__

elseStatement %= G.Epsilon
elseStatement %= elif__ + open_parenthesis__ + conditionalExpression + closed_parenthesis__ + expression + elseStatement
elseStatement %= else__ + expression

loop %= while__ + open_parenthesis__ + conditionalExpression + closed_parenthesis__ + expression
loop %= for__ + open_parenthesis__ + id__ + in__ + expression + closed_parenthesis__ + expression

variableDeclaration %= let__ + variableAssign + in__ + expression

variableAssign %= id__ + inicialization__ + expression
variableAssign %= id__ + inicialization__ + expression + comma__ + variableAssign
variableAssign %= id__ + checkingType + inicialization__ + expression
variableAssign %= id__ + checkingType + inicialization__ + expression + comma__ + variableAssign

#! factor <=> id__??
destructiveAssignment %= id__ + assignation__ + expression

inlineMethodList %= id__ + methodCall + func_arrow__ + expressionLine
inlineMethodList %= id__ + methodCall + func_arrow__ + expressionLine + inlineMethodList

typeInstantiating %= new__ + id__ + open_parenthesis__ + parameterList + closed_parenthesis__

downcasting %= as__ + id__

vector %= open_square_braket__ + parameterList + close_square_braket__
vector %= open_square_braket__ + expression + bars__ + id__ + in__ + expression + close_square_braket__

vectorCall %= open_square_braket__ + expression + close_square_braket__
