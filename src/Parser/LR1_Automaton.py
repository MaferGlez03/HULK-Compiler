from cmp.utils import ContainerSet
from cmp.pycompiler import Item
from cmp.tools.parsing import compute_firsts, compute_local_first

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    # Compute lookahead for child items
    for item in item.Preview():
        first = compute_local_first(firsts, item)
        for i in first:
         lookaheads.add(i)
    assert not lookaheads.contains_epsilon
    # Build and return child items
    productions = next_symbol.productions
    return [Item(production, 0, lookaheads) for production in productions] 


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }



def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts ))

        changed = closure.update(new_items)
        
    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

from cmp.automata import State, multiline_formatter

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    print('Building automaton')
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    print('Firsts computed')
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    print('Closure computed')
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        #print(len(G.terminals + G.nonTerminals))
        for symbol in G.terminals + G.nonTerminals:
            #print('finding status',symbol)
            next = frozenset(goto_lr1(current_state.state, symbol, firsts))
            if len(next) == 0: continue
            next_state = State(next, True)
            if not next in visited.keys():
                pending.append(next)
                visited[next] = next_state
                current_state.add_transition(symbol.Name, next_state)
            else:
              current_state.add_transition(symbol.Name, visited[next])
    
    automaton.set_formatter(multiline_formatter)
    print('se construyó el automata')
    return automaton