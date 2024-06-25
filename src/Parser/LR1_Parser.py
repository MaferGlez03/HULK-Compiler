from.LR1_Automaton import build_LR1_automaton
from.ShiftReduceParser import ShiftReduceParser


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
        
        for node in automaton:
            idx = node.idx
            for item in node.state:
                #print('current item', item)
                # Your code here!!!
                # - Fill self.Action and self.Goto according to item)
                
                    
                if  item.NextSymbol and item.NextSymbol.IsTerminal:
                    self._register(self.action, (idx, item.NextSymbol), (self.SHIFT,node.get(item.NextSymbol.Name).idx))
                    # self.action[idx, item.NextSymbol] = self.SHIFT,node.get(item.NextSymbol.Name).idx
                elif not item.NextSymbol and not item.production.Left == G.startSymbol:
                    
                    for lookahead in item.lookaheads:
                        self._register(self.action, (idx, lookahead), (self.REDUCE, item.production))
                        # self.action[idx, lookahead] = self.REDUCE, item.production
                
                elif item.IsReduceItem and item.production.Left == G.startSymbol and not item.NextSymbol:
                    
                    self._register(self.action, (idx, G.EOF), (self.OK, self.OK))

                else: #item.NextSymbol and item.NextSymbol.IsNonTerminal:
                    self._register(self.goto, (idx, item.NextSymbol), node.get(item.NextSymbol.Name).idx)
                
     
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value