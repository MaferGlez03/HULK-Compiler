class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        # Can add modifications to improve
        while True:
            state = stack[-1]
            lookahead = w[cursor]  # Maybe here I should put
            # if self.verbose: print(stack, '<---||--->', w[cursor:])

            if (state, lookahead) not in self.action:
                return None

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
