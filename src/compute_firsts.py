from cmp.pycompiler import *
from cmp.utils import ContainerSet

# Computes First(alpha)


def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
        return first_alpha

    for item in alpha:
        first_item = firsts[item]
        first_alpha.update(first_item)
        if (not first_item.contains_epsilon):
            break

    return first_alpha

# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha


def compute_firsts(G):
    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            first_X = firsts[X]
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    return firsts
