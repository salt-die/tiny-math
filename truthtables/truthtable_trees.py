"""
Generate Truth Tables from boolean expressions.

Example usage:
In [101]: tt = TruthTable('p and (~q or (p and r))', 'p or (q and r)', '(p or q) and (p or r)')

In [102]: tt.display()
┌───┬───┬───┬─────────────────────────┬────────────────┬───────────────────────┐
│ p │ q │ r │ p and (~q or (p and r)) │ p or (q and r) │ (p or q) and (p or r) │
├───┼───┼───┼─────────────────────────┼────────────────┼───────────────────────┤
│ F │ F │ F │            F            │       F        │           F           │
│ F │ F │ T │            F            │       F        │           F           │
│ F │ T │ F │            F            │       F        │           F           │
│ F │ T │ T │            F            │       T        │           T           │
│ T │ F │ F │            T            │       T        │           T           │
│ T │ F │ T │            T            │       T        │           T           │
│ T │ T │ F │            F            │       T        │           T           │
│ T │ T │ T │            T            │       T        │           T           │
└───┴───┴───┴─────────────────────────┴────────────────┴───────────────────────┘

In [103]: tt2 = tt.pop(); tt3 = tt.pop()

In [104]: tt2
Out[104]: (p or q) and (p or r)

In [105]: tt3
Out[105]: p or (q and r)

In [106]: tt2 == tt3
Out[106]: True

In [107]: tt + tt2
Out[107]: p and (~q or (p and r)) | (p or q) and (p or r)

In [108]: tt.trees[0].r
Out[108]: ~q or (p and r)

In [109]: tt.trees[0].r.r
Out[109]: p and r

In [110]: tt.trees[0].r.r.l
Out[110]: p

Operator precedence is parens, negate, then left-to-right.
"""
from functools import reduce
from itertools import filterfalse, product

from table_maker import table_maker
from expressions import TRUE, FALSE, Var, Negate, And, Or, Implies, Iff, Xor



OP_DICT = {'and': lambda p, q: And(p, q),
            'or': lambda p, q: Or(p, q),
            '->': lambda p, q: Implies(p, q),
           '<->': lambda p, q: Iff(p, q),
           'xor': lambda p, q: Xor(p, q)}

TOKENS = set(OP_DICT).union('~()TF')
TRUE = TRUE()
FALSE = FALSE()


def reformat(formula):
    """Add spaces around each parens and negate and split the formula."""
    formula = ''.join(f' {i} ' if i in '~()' else i for i in formula)
    return formula.split()

def find_vars(expression):
    """Return a set of variables in the expression."""
    return set(filterfalse(TOKENS.__contains__, expression))

def build_tree(expression):
    """Recursively build a parse tree starting with inner most parens."""
    if len(expression) == 1: # Base
        p = expression[0]
        return p

    if '(' in expression:
        # To find inner parens, we look for the first occurence of a close parens and then reverse
        # search to find the opening parens.
        last = expression.index(')')
        first = last - expression[last::-1].index('(')
        expression[first: last + 1] = [build_tree(expression[first + 1: last])]
        return build_tree(expression)

    if '~' in expression:
        negate_index = len(expression) - expression[::-1].index('~') - 1 # Find last negate.
        val = expression[negate_index + 1]
        expression[negate_index: negate_index + 2] = [Negate(val)]
        return build_tree(expression)

    p, op, q = expression[:3]
    op = OP_DICT[op]
    expression[:3] = [op(p, q)]
    return build_tree(expression)

def expr_to_tree(expression):
    """Generate a tree from a reformatted proposition."""
    # Replace constants and variables with Const and Vars
    for i, token in enumerate(expression):
        if token == 'T':
            expression[i] = TRUE
        elif token == 'F':
            expression[i] = FALSE
        elif token not in TOKENS:
            expression[i] = Var(token)

    return build_tree(expression)


class TruthTable:
    def __init__(self, *props):
        self.props = list(props)

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, new_props):
        self._props = list(new_props)
        self._update_attributes()

    def add_prop(self, prop):
        self._props.append(prop)
        self._update_attributes()

    def pop(self, i=None):
        prop = self._props.pop() if i is None else self._props.pop(i)
        self._update_attributes()
        return TruthTable(prop)

    def _update_attributes(self):
        expressions = tuple(map(reformat, self.props))
        self.vars = sorted(reduce(set.union, map(find_vars, expressions)))
        self.trees = list(map(expr_to_tree, expressions))

        self.table = []
        for values in product((False, True), repeat=len(self.vars)):
            vars_values = dict(zip(self.vars, values))
            results = [tree(**vars_values) for tree in self.trees]
            self.table.append(list(values) + results)

    def display(self, binary=False):
        translate = '01' if binary else 'FT'
        table = [[translate[i] for i in row] for row in self.table]
        table = table_maker(self.vars + self.props, *table)
        print(table)

    def __repr__(self):
        return ' | '.join(self.props)

    def __eq__(self, other):
        return (isinstance(other, TruthTable)
                and self.vars == other.vars
                and self.table == other.table)

    def __add__(self, other):
        if isinstance(other, str):
            return TruthTable(*self.props, other)
        return TruthTable(*self.props, *other.props)

    def __iadd__(self, other):
        if isinstance(other, str):
            self.add_prop(other)
        else:
            self.props = self.props + other.props
        return self
