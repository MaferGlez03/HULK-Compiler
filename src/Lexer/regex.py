import tokens

class MalformedRegexError(Exception):
    def __init__(self, message="La expresión regular está mal formada"):
        self.message = message
        super().__init__(self.message)

class DFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = {}  # Transitions for DFA

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state

    def accepts(self, input_string: str) -> bool:
        """
        Verifica si el DFA acepta la cadena de entrada.
        
        :param input_string: Cadena de entrada.
        :return: True si el DFA acepta la cadena, False en caso contrario.
        """
        current_state = self.start_state
        for symbol in input_string:
            if current_state in self.transitions and symbol in self.transitions[current_state]:
                current_state = self.transitions[current_state][symbol]
            else:
                return False  # No hay transición para el símbolo actual
        return current_state in self.accept_states
    
    def move(self, state, symbol):
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        else:
            raise Exception("No existe esa transicion")
        
    def get_token(self, dfa_state):
        tokens_set = set()
        if dfa_state in self.accept_states:
            for nfa_state in dfa_state:
                if nfa_state.token_recognized != None:
                    tokens_set.add(nfa_state.token_recognized.value)
        else:
            raise Exception("No es un estado final del DFA")
        value =  max(tokens_set)

        return tokens.TokenType(value).name
                




class State:
    def __init__(self):
        """
        Inicializa un estado creando un diccionario de transiciones donde
        el key es el simbolo y el value es el conjunto de estados para los cuales
        hay una transicion con ese simbolo
        """
        self.transitions = {}
        self.token_recognized = None
    

class NFA:
    def __init__(self, start_state: State, accept_states: set):
        self.start_state = start_state
        self.accept_states = accept_states
        

    def add_transition(self, from_state: State, symbol: str, to_states: set):
        """
        Parametros:
        from_state: Estado al que se le annadira la transicion
        symbol: Simbolo de la transicion
        to_states: Conjunto de estados a los que se transicionara con ese simbolo
        """
        if symbol not in from_state.transitions:
            from_state.transitions[symbol] = set()
        from_state.transitions[symbol].update(to_states)

    def epsilon_closure(self, states: set) -> set:
        """
        Calcula el cierre epsilon (closure) para un conjunto de estados.
        
        :param states: Conjunto de estados.
        :return: El cierre epsilon como un conjunto de estados.
        """
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            if '' in state.transitions:  # epsilon transitions are represented with an empty string
                for next_state in state.transitions['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def accepts(self, input_string: str) -> bool:
        """
        Verifica si el NFA acepta la cadena de entrada.
        
        param input_string: Cadena de entrada.
        return: True si el NFA acepta la cadena, False en caso contrario.
        """
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    next_states.update(state.transitions[symbol])
            current_states = self.epsilon_closure(next_states)
        return any(state in self.accept_states for state in current_states)
    
    def nfa2dfa(self):
        start_closure = self.epsilon_closure({self.start_state})
        start_state = frozenset(start_closure)
        unmarked_states = [start_state]
        dfa_transitions = {}
        dfa_accept_states = set()
        dfa_states = {start_state}

        while unmarked_states:
            current = unmarked_states.pop()
            dfa_transitions[current] = {}

            for symbol in {symbol for state in current for symbol in state.transitions if symbol}:  # All symbols excluding epsilon
                next_state = set()
                for nfa_state in current:
                    if symbol in nfa_state.transitions:
                        next_state.update(nfa_state.transitions[symbol])
                epsilon_closure = self.epsilon_closure(next_state)
                next_state_frozenset = frozenset(epsilon_closure)

                if next_state_frozenset not in dfa_states:
                    dfa_states.add(next_state_frozenset)
                    unmarked_states.append(next_state_frozenset)

                dfa_transitions[current][symbol] = next_state_frozenset

                if any(state in self.accept_states for state in epsilon_closure):
                    dfa_accept_states.add(next_state_frozenset)

        dfa = DFA(start_state, dfa_accept_states)
        for from_state, transitions in dfa_transitions.items():
            for symbol, to_state in transitions.items():
                dfa.add_transition(from_state, symbol, to_state)


        return dfa

    @staticmethod
    def concat(nfa1, nfa2):
        start_state = nfa1.start_state
        accept_states = nfa2.accept_states
        new_nfa = NFA(start_state, accept_states)
        for final_state in nfa1.accept_states:
            new_nfa.add_transition(from_state=final_state, symbol='', to_states={nfa2.start_state})
        return new_nfa
    
    @staticmethod
    def union(nfa1, nfa2):
        start_state = State()
        accept_state = State()
        new_nfa = NFA(start_state, {accept_state})
        new_nfa.add_transition(from_state=start_state, symbol='', to_states={nfa1.start_state, nfa2.start_state})
        for nfa in [nfa1, nfa2]:
            for final_state in nfa.accept_states:
                nfa.add_transition(from_state=final_state, symbol='', to_states={accept_state})
        return new_nfa
    
    @staticmethod
    def kleene_star(nfa):
        start_state = State()
        accept_state = State()
        new_nfa = NFA(start_state, {accept_state})

        new_nfa.add_transition(from_state=start_state, symbol='', to_states={nfa.start_state, accept_state})
        for final_state in nfa.accept_states:
            nfa.add_transition(from_state=final_state, symbol='', to_states={nfa.start_state, accept_state})
        
        return new_nfa
    
    @staticmethod
    def create_nfa(symbols: str):
        start_state = State()
        actual_state = start_state
        for i in range(len(symbols)):
            new_state = State()
            actual_state.transitions[symbols[i]] = {new_state}
            actual_state = new_state
        nfa = NFA(start_state, {new_state})
        return nfa

    



def infix2postfix(regex):
    operators_precedence= {'*': 3, '?':2, '|':1} #mientras mayor sea el key mayor es la precedencia
    output_queue = []
    operators_stack = []

    for symbol in regex:
        # En caso de que el simbolo actual tenga menor precedencia que el que esta en el tope del stack entonces hago pop al tope del stack y voy annadiendo eso al output hasta que el stack se quede vacio o quede un operador con menor precedencia que el actual en el top del stack
        if (symbol in operators_precedence) and (operators_stack) and (operators_stack[-1] in operators_precedence):
            while(operators_stack and operators_stack[-1] in operators_precedence and operators_precedence[operators_stack[-1]] >= operators_precedence[symbol]):
                top_stack = operators_stack.pop()
                output_queue.append(top_stack)
            operators_stack.append(symbol)
        #En caso de que el simbolo sea un operador o un '(' annado eso al stack
        elif symbol in operators_precedence or symbol == '(':
            operators_stack.append(symbol)
        #En caso de que sea un ')' voy popeando los elementos del stack y annadiendolos al output hasta encontrar un '(' y luego deshecho los 2  parentesis
        elif symbol == ')':
            while(True):
                if not operators_stack:
                    raise MalformedRegexError()
                top_stack = operators_stack.pop()
                if top_stack != '(':
                    output_queue.append(top_stack)
                else:
                    break
        #Si es cualquier otro tipo de simbolo se annade al output       
        else:
            output_queue.append(symbol)

    while(operators_stack):
        top_stack = operators_stack.pop()
        output_queue.append(top_stack)
    
    return output_queue

def regex2nfa(regex):
    postfix_regex = infix2postfix(regex)
    nfa_stack = []

    for symbol in postfix_regex:
        if symbol == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            new_nfa = NFA.union(nfa1, nfa2)
            nfa_stack.append(new_nfa)
        elif symbol == '?':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            new_nfa = NFA.concat(nfa1, nfa2)
            nfa_stack.append(new_nfa)
        elif symbol == '*':
            nfa = nfa_stack.pop()
            new_nfa = NFA.kleene_star(nfa)
            nfa_stack.append(new_nfa)
        else:
            new_nfa = NFA.create_nfa(symbol)
            nfa_stack.append(new_nfa)
        
    final_nfa = nfa_stack.pop()
    return final_nfa    



