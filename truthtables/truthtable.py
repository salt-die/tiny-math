from expressions import *
from functools import reduce
from itertools import filterfalse, product

OP_DICT = {'and': lambda p, q: And(p, q),
            'or': lambda p, q: Or(p, q),
            '->': lambda p, q: Implies(p, q),
           '<->': lambda p, q: Iff(p, q),
           'xor': lambda p, q: Xor(p, q)}

TRUE = TRUE()
FALSE = FALSE()
TOKENS = set(OP_DICT).union('~()')


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

def table_maker(*rows):
    """Generates an aligned table. Modified from https://github.com/salt-die/Table-Maker"""
    rows = list(rows)

    # Pad the length of items in each column
    lengths = tuple(map(len, rows[0]))
    for i, row in enumerate(rows):
        for j, (item, length) in enumerate(zip(row, lengths)):
            rows[i][j] = f'{item:^{length}}'

    # Make separators
    horizontals = tuple("─" * (length + 2) for length in lengths)
    top, title, bottom = (f'{l}{m.join(horizontals)}{r}' for l, m, r in ('┌┬┐', '├┼┤', '└┴┘'))

    table = [f'│ {" │ ".join(row)} │' for row in rows]
    table.insert(0, top)
    table.insert(2, title)
    table.append(bottom)
    table = '\n'.join(table)
    return table


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
