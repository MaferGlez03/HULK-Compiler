import regex
import tokens

class HULK_Lexer:
    def __init__(self):
        self.automaton = self.build_automaton()
        print("DFA BUILT")

    def build_automaton(self):
        hulk_tokens = tokens.hulk_tokens()

        nfas = []
        for (token_type, pattern) in hulk_tokens:
            if token_type in tokens.special_tokens:
                nfa = regex.NFA.create_nfa(pattern)
            else:
                nfa = regex.regex2nfa(pattern)

            for accept_state in nfa.accept_states:
                accept_state.token_recognized = token_type

            nfas.append(nfa)

        start_state = regex.State()
        
        nfa_combination = regex.NFA(start_state=start_state, accept_states=set())

        for nfa in nfas:
            nfa_combination.add_transition(from_state=start_state, symbol='', to_states={nfa.start_state})
            nfa_combination.accept_states.update(nfa.accept_states)

        print("NFA COMBINATION COMPLETED")
        
        dfa = nfa_combination.nfa2dfa()

        print("NFA TO DFA COMPLETED")

        return dfa
    
    def tokenize(self, code: str) -> list:
        code += '$'
        code_tokenized = []
        lexemeBegin = 0
        forward = 0
        actual_lexeme = ""
        actualState = self.automaton.start_state
        last_token_recognized = None
        last_lexeme_recognized = None
        last_lexeme_position = -1

        while lexemeBegin < len(code) and code[lexemeBegin] != '$':
            if forward >= len(code):
                break
            symbol = code[forward]
            actual_lexeme += symbol

            if symbol not in self.automaton.transitions.get(actualState, {}):
                if last_token_recognized is not None:
                    code_tokenized.append((last_token_recognized, last_lexeme_recognized))
                    lexemeBegin = last_lexeme_position + 1
                else:
                    # Handle error or unrecognized symbol
                    lexemeBegin += 1
                forward = lexemeBegin
                actual_lexeme = ""
                actualState = self.automaton.start_state
                last_token_recognized = None
                last_lexeme_recognized = None
                last_lexeme_position = -1
            else:
                actualState = self.automaton.move(actualState, symbol)
                if actualState in self.automaton.accept_states:
                    last_token_recognized = self.automaton.get_token(actualState)
                    last_lexeme_recognized = actual_lexeme
                    last_lexeme_position = forward
                forward += 1

        if last_token_recognized is not None:
            code_tokenized.append((last_token_recognized, last_lexeme_recognized))

        return code_tokenized


lexer = HULK_Lexer()
code_tokenized = lexer.tokenize("let x = 5; \n cadena = \"tu mama te ama\"")
print(code_tokenized)





