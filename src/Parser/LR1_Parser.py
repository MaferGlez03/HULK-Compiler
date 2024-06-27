from.LR1_Automaton import build_LR1_automaton
from.ShiftReduceParser import ShiftReduceParser


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        print('Building table')
        
        for i, node in enumerate(automaton):
            node.idx = i
        
        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.NextSymbol and item.NextSymbol.IsTerminal:
                    self._register(self.action, (idx, item.NextSymbol), (self.SHIFT, node.get(item.NextSymbol.Name).idx), item)
                elif not item.NextSymbol and not item.production.Left == G.startSymbol:
                    for lookahead in item.lookaheads:
                        self._register(self.action, (idx, lookahead), (self.REDUCE, item.production), item)
                elif item.IsReduceItem and item.production.Left == G.startSymbol and not item.NextSymbol:
                    self._register(self.action, (idx, G.EOF), (self.OK, self.OK), item)
                else:
                    self._register(self.goto, (idx, item.NextSymbol), node.get(item.NextSymbol.Name).idx, item)
    
    @staticmethod
    def _register(table, key, value, item):
        if key in table:
            existing_value = table[key]
            if existing_value != value:
                if existing_value[0] == 'SHIFT' and value[0] == 'REDUCE':
                    raise Exception('Shift-Reduce conflict at item:', item, 'with key:', key)
                elif existing_value[0] == 'REDUCE' and value[0] == 'REDUCE':
                    raise Exception('Reduce-Reduce conflict at item:', item, 'with key:', key)
        else:
            table[key] = value
