from cmp.pycompiler import *
from cmp.utils import ContainerSet

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            for i, symbol in enumerate(alpha):
                if(symbol.IsTerminal):
                    continue
                
                if(symbol.IsNonTerminal):
                    if( i + 1 < len(alpha)):
                        
                        beta = alpha[i+1:]
                        for symbol1 in beta :

                            try:
                                local_first = local_firsts[symbol1]
                            except KeyError:
                                local_first = local_firsts[symbol1] = firsts[symbol1]
                           
                               
                            change |= follows[symbol].update(local_first)
                            if(local_first.contains_epsilon):
                                change |= follows[symbol].update(follow_X)
                    else: 
                        change |= follows[symbol].update(follow_X)
    return follows