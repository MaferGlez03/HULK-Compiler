from cmp.pycompiler import Grammar
from .H_ast import *

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
program %= definitionList + globalExpression, lambda h, s: ProgramNode(s[1], s[2]), None, None

definitionList %= G.Epsilon, lambda h, s: []
definitionList %= definition + definitionList, lambda h, s: [s[1]] + s[2], None, None 

definition %= functionDefinition, lambda h, s: s[1]
definition %= typeDefinition, lambda h, s: s[1]
definition %= protocolDefinition, lambda h, s: s[1]

functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + func_arrow__ + expression + semicolon__, lambda h, s: FunctionDeclNode(s[2], s[4], s[7])
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + expressionBlock, lambda h, s: FunctionDeclNode(s[2], s[4], s[6])
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + func_arrow__ + expression + semicolon__, lambda h, s: FunctionDeclNode(s[2], s[4], s[9], s[7])
functionDefinition %= function__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + expressionBlock, lambda h, s: FunctionDeclNode(s[2], s[4], s[8], s[7])

methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + func_arrow__ + expression + semicolon__, lambda h,s: FunctionDeclNode(s[1], s[3], s[6])
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + expressionBlock, lambda h,s: FunctionDeclNode(s[1], s[3], s[5])
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + func_arrow__ + expression + semicolon__, lambda h,s: FunctionDeclNode(s[1], s[3], s[8], s[6])
methodDefinition %= id__ + open_parenthesis__ + idList + closed_parenthesis__ + type_asignator__ + id__ + expressionBlock, lambda h,s: FunctionDeclNode(s[1], s[3], s[7], s[6])

idList %= G.Epsilon, lambda h,s: []
idList %= idMultiple, lambda h,s: s[1]

idMultiple %= id__, lambda h,s: [VariableDeclNode(s[1], None, None)]
idMultiple %= id__ + type_asignator__ + id__, lambda h,s: [VariableDeclNode(s[1], s[3], None)]
idMultiple %= id__ + comma__ + idMultiple, lambda h,s: [VariableDeclNode(s[1], None, None)] + s[3]
idMultiple %= id__ + type_asignator__ + id__ + comma__ + idMultiple, lambda h,s: [VariableDeclNode(s[1], s[3], None)] + s[5]

typeDefinition %= type__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[4], None, None, None)
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[7], None, s[4], None)
typeDefinition %= type__ + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[6], s[4], None, None)
typeDefinition %= type__ + id__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[9], s[4], None, s[6])
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[9], s[7], s[4], None)
typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__, lambda h,s: TypeDeclNode(s[2], s[12], s[7], s[4], s[9])
# typeDefinition %= type__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList +closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__
# typeDefinition %= type__ + id__ + open_parenthesis__ + idList + closed_parenthesis__ + inherits__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__ + open_curly_bracket__ + attributeList + closed_curly_bracket__ + semicolon__

attributeList %= G.Epsilon, lambda h, s: []
attributeList %= attribute + attributeList, lambda h, s: [s[1]] + s[2]

attribute %= id__ + inicialization__ + expression + semicolon__, lambda h, s: VariableDeclNode(s[1], None, s[3])
attribute %= id__ + type_asignator__ + id__ + inicialization__ + expression + semicolon__, lambda h, s: VariableDeclNode(s[1], s[3], s[5])
attribute %= methodDefinition, lambda h, s: s[1]

protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__, lambda h, s: ProtocolDeclNode(s[2], [s[4]] + s[5], None)
protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__, lambda h, s: ProtocolDeclNode(s[2], [s[6]] + s[7], s[4])
# protocolDefinition %= protocol__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__ + semicolon__
# protocolDefinition %= protocol__ + id__ + extends__ + id__ + open_curly_bracket__ + inlineMethod + inlineMethodList + closed_curly_bracket__ + semicolon__

inlineMethodList %= G.Epsilon, lambda h, s: []
inlineMethodList %= inlineMethod + inlineMethodList, lambda h, s: [s[1]] + s[2]

inlineMethod %= id__ + open_parenthesis__ + parameterType + closed_parenthesis__ + type_asignator__ + id__ + semicolon__, lambda h, s: FunctionDeclNode(s[1], s[3], None, s[6])

parameterType %= G.Epsilon, lambda h, s: []
parameterType %= parameterTypeList, lambda h, s: s[1]

parameterTypeList %= id__ + type_asignator__ + id__, lambda h, s: [VariableDeclNode(s[1], s[3], None)]
parameterTypeList %= id__ + type_asignator__ + id__ + comma__ + parameterTypeList, lambda h, s: [VariableDeclNode(s[1], s[3], None)] + s[5]

globalExpression %= expression + semicolon__ , lambda h, s: s[1]
globalExpression %= expressionBlock, lambda h, s: s[1]

expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__, lambda h, s: ExpBlockNode(s[2])
# expressionBlock %= open_curly_bracket__ + expressionLineList + closed_curly_bracket__ + semicolon__

expressionLineList %= expression + semicolon__, lambda h, s: [s[1]]
expressionLineList %= expression + semicolon__ + expressionLineList, lambda h, s: [s[1]] + s[3]

expression %= stringExpression, lambda h, s: s[1]
expression %= new__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__, lambda h, s: NewExpNode(s[2], s[4])
expression %= factor + assignation__ + expression, lambda h, s: AssignExpNode(s[1], s[3])
expression %= let__ + variableAssign + in__ + expression, lambda h, s: LetExpNode(s[2], s[4])
expression %= while__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression, lambda h, s: WhileExpNode(s[3], s[5])
expression %= for__ + open_parenthesis__ + id__ + in__ + expression + closed_parenthesis__ + expression, lambda h, s: ForExpNode(s[3], s[5], s[7])
expression %= if__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression + elifStatement + else__ + expression, lambda h, s: IfExpNode(s[3], s[5], s[6], s[8])

stringExpression %= stringExpression1, lambda h, s: s[1]
stringExpression %= stringExpression1 + as__ + id__, lambda h, s: AsNode(s[1], s[3])

elifStatement %= G.Epsilon, lambda h, s: []
elifStatement %= elif__ + open_parenthesis__ + stringExpression2 + closed_parenthesis__ + expression + elifStatement, lambda h, s: [IfExpNode(s[3], s[5], None, None)] + s[6]

variableAssign %= id__ + inicialization__ + expression, lambda h, s: [VariableDeclNode(s[1], None, s[3])]
variableAssign %= id__ + type_asignator__ + id__ + inicialization__ + expression, lambda h, s: [VariableDeclNode(s[1], s[3], s[5])]
variableAssign %= id__ + inicialization__ + expression + comma__ + variableAssign, lambda h, s: [VariableDeclNode(s[1], None, s[3])] + s[5]
variableAssign %= id__ + type_asignator__ + id__ + inicialization__ + expression + comma__ + variableAssign, lambda h, s: [VariableDeclNode(s[1], s[3], s[5])] + s[7]

stringExpression1 %= stringExpression2, lambda h, s: s[1]
stringExpression1 %= stringExpression1 + string_operator__ + stringExpression2, lambda h, s: ConcatNode(s[1], s[3])
stringExpression1 %= stringExpression1 + string_operator_space__ + stringExpression2, lambda h, s: ConcatSpaceNode(s[1], s[3])

stringExpression2 %= stringExpression3, lambda h, s: s[1]
stringExpression2 %= stringExpression2 + and__ + stringExpression3, lambda h, s: AndNode(s[1], s[3])

stringExpression3 %= conditionalExpression, lambda h, s: s[1]
stringExpression3 %= stringExpression3 + or__ + conditionalExpression, lambda h, s: OrNode(s[1], s[3])

conditionalExpression %= condition, lambda h, s: s[1]
conditionalExpression %= not__ + condition, lambda h, s: NotNode(s[2])

condition %= arithmeticExpression, lambda h, s: s[1]
condition %= arithmeticExpression + neq__ + arithmeticExpression, lambda h, s: NotEqualNode(s[1], s[3])
condition %= arithmeticExpression + lt__ + arithmeticExpression, lambda h, s: LessThanNode(s[1], s[3])
condition %= arithmeticExpression + eq__ + arithmeticExpression, lambda h, s: EqualNode(s[1], s[3])
condition %= arithmeticExpression + gt__ + arithmeticExpression, lambda h, s: GreaterThanNode(s[1], s[3])
condition %= arithmeticExpression + lte__ + arithmeticExpression, lambda h, s: LessThanEqualNode(s[1], s[3])
condition %= arithmeticExpression + gte__ + arithmeticExpression, lambda h, s: GreaterThanEqualNode(s[1], s[3])
condition %= arithmeticExpression + is__ + id__, lambda h, s: IsNode(s[1], s[3])

arithmeticExpression %= term, lambda h, s: s[1]
arithmeticExpression %= arithmeticExpression + plus_operator__ + term, lambda h, s: PlusNode(s[1], s[3])
arithmeticExpression %= arithmeticExpression + minus_operator__ + term, lambda h, s: MinusNode(s[1], s[3])

term %= neg, lambda h, s: s[1]
term %= term + division__ + neg, lambda h, s: DivisionNode(s[1], s[3])
term %= term + module_operation__ + neg, lambda h, s: ModuleNode(s[1], s[3])
term %= term + multiplication__ + neg, lambda h, s: MultiplicationNode(s[1], s[3])

neg %= power, lambda h, s: s[1]
neg %= minus_operator__ + neg, lambda h, s: NegNode(s[2])

power %= factor, lambda h, s: s[1]
power %= factor + exponentiation__ + power, lambda h, s: PowerNode(s[1], s[3])

factor %= atom, lambda h, s: s[1]
factor %= factor + dot__ + id__ + open_parenthesis__ + argumentList + closed_parenthesis__, lambda h, s: PropertyCallNode(s[1], s[3], s[5])
factor %= factor + dot__ + id__, lambda h, s: AttributeCallNode(s[1], s[3])
factor %= factor + open_square_braket__ + expression + close_square_braket__, lambda h, s: IndexExpNode(s[1], s[3])

atom %= id__, lambda h, s: VariableNode(s[1])
atom %= number__, lambda h, s: NumberNode(s[1])
atom %= booleanValue__, lambda h, s: BooleanNode(s[1])
atom %= string__, lambda h, s: StringNode(s[1])
atom %= id__ + open_parenthesis__ + argumentList + closed_parenthesis__, lambda h, s: FunctCallNode(s[1], s[3])
atom %= expressionBlock, lambda h, s: s[1]
atom %= open_parenthesis__ + expression + closed_parenthesis__, lambda h, s: s[2]
atom %= open_square_braket__ + argumentList + close_square_braket__, lambda h, s: VectorNode(s[2])
atom %= open_square_braket__ + expression + bars__ + id__ + in__ + expression + close_square_braket__, lambda h, s: VectorIterableNode(s[2], s[4], s[6])

argumentList %= G.Epsilon, lambda h, s: []
argumentList %= expression + argumentList2, lambda h, s: [s[1]] + s[2]

argumentList2 %= G.Epsilon, lambda h, s: []
argumentList2 %= comma__ + expression + argumentList2, lambda h, s: [s[2]] + s[3]
