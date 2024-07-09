from Tools.errors import *
class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, action= None, goto = None, verbose=False):
        self.G = G
        self.verbose = verbose
        if action is None or goto is None:
            self.action = {}
            self.goto = {}
            self._build_parsing_table()
        else:
            self.action = action
            self.goto = goto

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            current = w[cursor]
            lookahead = w[cursor].token_type 
            #if self.verbose: print(stack, '<---||--->', w[cursor:])
           
            if(state,lookahead) not in self.action:
                return (errors(current.row,current.column,f'Unexpected token {current.lex}','Parsing Error'),None)
            
            
            action, tag = self.action[state, lookahead]

            if action == self.SHIFT:
                operations.append(self.SHIFT)
                stack.append(tag)
                cursor += 1

            elif action == self.REDUCE:
                operations.append(self.REDUCE)
                output.append(tag)
                left, right = tag
                for symbol in right:
                    stack.pop()

                state = stack[-1]
                goto = self.goto[state, left]
                stack.append(self.goto[stack[-1], left])
            elif action == self.OK:  # Check table
                stack.pop()
                assert len(stack) == 1
                return output if not get_shift_reduce else (output, operations)
            else:
                raise Exception('Not Valid')
