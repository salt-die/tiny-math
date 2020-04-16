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

In [108]: tt.exprs[0].r
Out[108]: ~q or (p and r)

In [109]: tt.exprs[0].r.r
Out[109]: p and r

In [110]: tt.exprs[0].r.r.l
Out[110]: p

Operator precedence is `~`, `()`, `and`, then left-to-right.
"""
from itertools import product
from table_maker import table_maker
from parser_lexer import LogicLexer, LogicParser

LEXER = LogicLexer()
PARSER = LogicParser()


class TruthTable:
    def __init__(self, *props):
        self.props = props

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
        PARSER.vars = set()
        self.exprs = [PARSER.parse(LEXER.tokenize(prop)) for prop in self.props]
        self.vars = sorted(PARSER.vars)

        self.table = []
        for values in product((False, True), repeat=len(self.vars)):
            vars_values = dict(zip(self.vars, values))
            results = [expr(**vars_values) for expr in self.exprs]
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
