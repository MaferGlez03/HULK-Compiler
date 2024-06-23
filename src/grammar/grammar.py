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
statement = G.NonTerminal('<statement>')
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
typeMethod = G.NonTerminal('<typeMethod>')
typeInheritance = G.NonTerminal('<typeInheritance>')
checkingType = G.NonTerminal('<checkingType>')
testingType = G.NonTerminal('<testingType>')
downcasting = G.NonTerminal('<downcasting>')
protocolDefinition = G.NonTerminal('<protocolDefinition>')
vector = G.NonTerminal('<vector>')
parameterList = G.NonTerminal('<parameterList>')
parameter = G.NonTerminal('<parameter>')
expressionList = G.NonTerminal('<expressionList>')

# terminals
open_parenthesis = G.Terminal('(')
closed_parenthesis = G.Terminal(')')
open_curly_bracket = G.Terminal('{')
closed_curly_bracket = G.Terminal('}')
open_square_braket = G.Terminal('[')
close_square_braket = G.Terminal(']')

semicolon = G.Terminal(';')
comma = G.Terminal(',')
dot = G.Terminal('.')
type_asignator = G.Terminal(':')

function = G.Terminal('function')
while_ = G.Terminal('while')
for_ = G.Terminal('for')
let = G.Terminal('let')
in_ = G.Terminal('in')
is_ = G.Terminal('is')
as_ = G.Terminal('as')

ID = G.Terminal('ID')
number = G.Terminal('number')
string_= G.Terminal('string')
new = G.Terminal('new')
type = G.Terminal('type')
protocol = G.Terminal('protocol')
extends = G.Terminal('extends')
inherits = G.Terminal('inherits')

assignation = G.Terminal(':=')
inicialization = G.Terminal('=')
func_arrow = G.Terminal('=>')

plus_operator = G.Terminal('+')
minus_operator = G.Terminal('-')
multiplication = G.Terminal('*')
division = G.Terminal('/')
exponentiation = G.Terminal('^')
module_operation = G.Terminal('%')

string_operator = G.Terminal('@')
string_operator_space = G.Terminal('@@')

if_ = G.Terminal('if')
elif_ = G.Terminal('elif')
else_ = G.Terminal('else')

and_ = G.Terminal('&')
or_ = G.Terminal('|')
not_ = G.Terminal('!')

true = G.Terminal('true')
false = G.Terminal('false')

gt = G.Terminal('>')
lt = G.Terminal('<')
gte = G.Terminal('>=')
lte = G.Terminal('<=')
eq = G.Terminal('==')
neq = G.Terminal('!=')

#productions
program %= globalExpression + G.EOF

globalExpression %= expression
globalExpression %= expressionBlock
globalExpression %= functionDefinitionList + globalExpression

expression %= arithmeticExpression
expression %= stringExpression
expression %= destructiveAssignment
expression %= functionCall
expression %= conditional
expression %= loop
expression %= variableDeclaration
expression %= typeInstantiating
expression %= checkingType + expression

arithmeticExpression %= arithmeticExpression + exponentiation + power 
arithmeticExpression %= power

power %= power + plus_operator + module
power %= power + minus_operator + module
power %= module

module %= module + module_operation + term
module %= term

term %= term + multiplication + factor
term %= term + division + factor
term %= factor

factor %= number
factor %= open_parenthesis + arithmeticExpression + closed_parenthesis

stringExpression %= stringLiteral
stringExpression %= stringLiteral + string_operator + concatenation
stringExpression %= stringLiteral + string_operator_space + concatenation

concatenation %= stringLiteral
concatenation %= stringLiteral + string_operator + concatenation
concatenation %= stringLiteral + string_operator_space + concatenation
concatenation %= number

stringLiteral %= string_

functionCall %= ID + open_parenthesis + argumentList + closed_parenthesis

argumentList %= expression + comma + argumentList
argumentList %= G.Epsilon

expressionBlock %= open_curly_bracket + statement + closed_curly_bracket + semicolon
expressionBlock %= open_curly_bracket + statement + closed_curly_bracket
expressionBlock %= open_curly_bracket + statmentList + closed_curly_bracket + semicolon
expressionBlock %= open_curly_bracket + statmentList + closed_curly_bracket

statmentList %= statement + semicolon
statmentList %= statement + semicolon + statmentList

statement %= expression + semicolon
statement %= variableDeclaration
statement %= functionDefinition
statement %= checkingType + expression + semicolon

conditional %= if_ + conditionalLine

conditionalLine %= open_parenthesis + conditionalExpression + closed_parenthesis + statement + elseStatement
conditionalLine %= open_parenthesis + conditionalExpression + closed_parenthesis + expressionBlock + elseStatement

conditionalExpression %= condition + and_ + conditionalExpression
conditionalExpression %= condition + or_ + conditionalExpression
conditionalExpression %= not_ + condition
conditionalExpression %= condition

condition %= comparation
condition %= open_parenthesis + comparation + closed_parenthesis
condition %= testingType
condition %= open_parenthesis + testingType + closed_parenthesis
condition %= booleanValue

booleanValue %= true
booleanValue %= false

comparation %= expression + lt + expression
comparation %= expression + gt + expression
comparation %= expression + lte + expression
comparation %= expression + gte + expression
comparation %= expression + eq + expression
comparation %= expression + neq + expression

elseStatement %= elif_ + conditionalLine
elseStatement %= else_ + statement
elseStatement %=  else_ + expressionBlock
elseStatement %= G.Epsilon

loop %= while_ + open_parenthesis + conditionalExpression + closed_parenthesis + statement
loop %= while_ + open_parenthesis + conditionalExpression + closed_parenthesis + expressionBlock
loop %= for_ + open_parenthesis + ID + in_ + expression + closed_parenthesis + statement
loop %=  for_ + open_parenthesis + ID + in_ + expression + closed_parenthesis + expressionBlock

variableDeclaration %= let + variableAssign + in_ + expression + semicolon
variableDeclaration %= let + variableAssign + in_ + open_parenthesis + expression + closed_parenthesis
variableDeclaration %= let + variableAssign + in_ + open_curly_bracket + expressionBlock + closed_curly_bracket
variableDeclaration %= let + variableAssign + downcasting + in_ + expression + semicolon
variableDeclaration %= let + variableAssign + downcasting + in_ + open_parenthesis + expression + closed_parenthesis
variableDeclaration %= let + variableAssign + downcasting + in_ + open_curly_bracket + expressionBlock + closed_curly_bracket

variableAssign %= ID + inicialization + expression
variableAssign %= ID + inicialization + expression + comma + variableAssign
variableAssign %= ID + checkingType + inicialization + expression
variableAssign %= ID + checkingType + inicialization + expression + comma + variableAssign

destructiveAssignment %= ID + assignation + expression + semicolon

functionDefinitionList %= functionDefinition
functionDefinitionList %= functionDefinition + functionDefinitionList

functionDefinition %= function + ID + open_parenthesis + idList + closed_parenthesis + func_arrow + expression
functionDefinition %= function + ID + open_parenthesis + idList + closed_parenthesis + expressionBlock

idList %= ID
idList %= ID + comma + idList
idList %= ID + checkingType
idList %= ID + checkingType + comma + idList
idList %= G.Epsilon

typeDefinition %= type + ID + open_curly_bracket + attributeList + methodsList + closed_curly_bracket
typeDefinition %= type + ID + inherits + ID + open_curly_bracket + attributeList + methodsList + closed_curly_bracket
typeDefinition %= type + ID + methodCall + open_curly_bracket + attributeList + methodsList + closed_curly_bracket
typeDefinition %= type + ID + methodCall + inherits + ID + open_curly_bracket + attributeList + methodsList + closed_curly_bracket

attributeList %= attribute + semicolon
attributeList %= attribute + semicolon + attributeList

attribute %= ID + inicialization + expression
attribute %= ID + checkingType + inicialization + expression

methodsList %= inlineMethodList
methodsList %= fullMethodList

inlineMethodList %= ID + methodCall + func_arrow + expression + semicolon
inlineMethodList %= ID + methodCall + func_arrow + expression + semicolon + inlineMethodList

fullMethodList %= ID + methodCall + func_arrow + expressionBlock + semicolon
fullMethodList %= ID + methodCall + func_arrow + expressionBlock + semicolon + fullMethodList

methodCall %= open_parenthesis + parameterList + closed_parenthesis

typeInstantiating %= new + ID + open_parenthesis + parameterList + closed_parenthesis

typeAtribute %= ID + dot + ID
typeAtribute %= ID + dot + ID + typeAtribute

typeMethod %= ID + dot + methodCall

typeInheritance %= inherits + ID

checkingType %= type_asignator + ID

testingType %= ID + is_ + ID

downcasting %= as_ + ID

protocolDefinition %= protocol + ID + open_curly_bracket + inlineMethodList + closed_curly_bracket
protocolDefinition %= protocol + ID + extends + ID + open_curly_bracket + inlineMethodList + closed_curly_bracket

vector %= open_square_braket + parameterList + close_square_braket
vector %= open_square_braket + expression + or_ + ID + in_ + expression + close_square_braket

parameterList %= parameter
parameterList %= parameter + comma + parameterList

expressionList %= expression
expressionList %= expression + comma + expressionList
