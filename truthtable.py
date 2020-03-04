"""
Generate Truth Tables from boolean expressions.

Example usage:
>>> tt = TruthTable('p and (~q or (p and r))', 'p or q and r', 'p -> q')

>>> tt.display()
┌───┬───┬───┬─────────────────────────┬──────────────┬────────┐
│ p │ q │ r │ p and (~q or (p and r)) │ p or q and r │ p -> q │
├───┼───┼───┼─────────────────────────┼──────────────┼────────┤
│ F │ F │ F │            F            │      F       │   T    │
│ F │ F │ T │            F            │      F       │   T    │
│ F │ T │ F │            F            │      F       │   T    │
│ F │ T │ T │            F            │      T       │   T    │
│ T │ F │ F │            T            │      F       │   F    │
│ T │ F │ T │            T            │      T       │   F    │
│ T │ T │ F │            F            │      F       │   T    │
│ T │ T │ T │            T            │      T       │   T    │
└───┴───┴───┴─────────────────────────┴──────────────┴────────┘

>>> tt.display(binary=True)
┌───┬───┬───┬─────────────────────────┬──────────────┬────────┐
│ p │ q │ r │ p and (~q or (p and r)) │ p or q and r │ p -> q │
├───┼───┼───┼─────────────────────────┼──────────────┼────────┤
│ 0 │ 0 │ 0 │            0            │      0       │   1    │
│ 0 │ 0 │ 1 │            0            │      0       │   1    │
│ 0 │ 1 │ 0 │            0            │      0       │   1    │
│ 0 │ 1 │ 1 │            0            │      1       │   1    │
│ 1 │ 0 │ 0 │            1            │      0       │   0    │
│ 1 │ 0 │ 1 │            1            │      1       │   0    │
│ 1 │ 1 │ 0 │            0            │      0       │   1    │
│ 1 │ 1 │ 1 │            1            │      1       │   1    │
└───┴───┴───┴─────────────────────────┴──────────────┴────────┘

Operator precendence is parens, negate, then left-to-right.
"""
from functools import reduce
from itertools import filterfalse, product

OP_DICT = {'and': lambda p, q: p and q,
            'or': lambda p, q: p or q,
            '->': lambda p, q: not p or q,
           '<->': lambda p, q: p == q,
           'xor': lambda p, q: p != q}

TOKENS = set(OP_DICT).union('~()')

def reformat(formula):
    """Add spaces around each parens and negate and split the formula."""
    formula = ''.join(f' {i} ' if i in '()~' else i for i in formula)
    return formula.split()

def generate(n):
    """Generate truth table values for n variables by iterating through binary numbers."""
    return map(list, product((0, 1), repeat=n))

def find_vars(expression):
    """Return a set of variables in the expression."""
    return set(filterfalse(TOKENS.__contains__, expression))

def evaluate(expression, vars_values):
    """Recursively evaluate expression starting with inner most parens."""
    if len(expression) == 1: # Base
        p = expression[0]
        return vars_values.get(p, p)

    expression = expression.copy() # We'll be modifying expression, so let's make a copy.
    if '(' in expression:
        # To find inner parens, we look for the first occurence of a close parens and then reverse
        # search to find the opening parens.
        last = expression.index(')')
        first = last - expression[last::-1].index('(')
        expression[first: last + 1] = [evaluate(expression[first + 1: last], vars_values)]
        return evaluate(expression, vars_values)

    if '~' in expression:
        negate_index = expression.index('~')
        var = expression[negate_index + 1]
        var = vars_values.get(var, var)
        expression[negate_index: negate_index + 2] = [int(not var)]
        return evaluate(expression, vars_values)

    p, op, q = expression[:3]
    p, op, q = vars_values.get(p, p), OP_DICT[op], vars_values.get(q, q)
    expression[:3] = [int(op(p, q))]
    return evaluate(expression, vars_values)

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
        self._props = list(props)
        self._update_attributes()

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
        expressions = [reformat(prop) for prop in self.props]

        self.vars = sorted(reduce(set.union, map(find_vars, expressions)))

        self.table = []
        for values in generate(len(self.vars)):
            vars_values = dict(zip(self.vars, values))
            results = [evaluate(expression, vars_values) for expression in expressions]
            self.table.append(values + results)

    def display(self, binary=False):
        translate = '01' if binary else 'FT'
        table = [[translate[value] for value in row] for row in self.table]
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
