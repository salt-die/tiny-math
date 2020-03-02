"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""
"""
Generate Truth Tables from boolean expressions.

Example usage:
>>> tt = TruthTable('p and (-q or (p and r))', 'p or q and r', 'p -> q')

>>> tt.display()
┌───┬───┬───┬─────────────────────────┬──────────────┬────────┐
│ p │ q │ r │ p and (-q or (p and r)) │ p or q and r │ p -> q │
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
│ p │ q │ r │ p and (-q or (p and r)) │ p or q and r │ p -> q │
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
"""
from itertools import zip_longest
from functools import reduce

def reformat(formula):
    """Add spaces around each parens and negate and split the formula."""
    formula = ''.join(f' {i} ' if i in '()' or (i == '-' and j != '>') else i
                      for i, j in zip_longest(formula, formula[1:]))
    return formula.split()

def generate(n):
    """Generate truth table values for n variables by iterating through binary numbers."""
    return [list(map(int, bin(i)[2:].zfill(n))) for i in range(2**n)]

def is_var(token):
    """Returns true if token is a variable."""
    return token not in {'and', 'or', '->', '<->', '-', '(', ')'}

def find_vars(expression):
    """Return a set of variables in the expression."""
    return set(filter(is_var, expression))

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

    if '-' in expression:
        negate_index = expression.index('-')
        var = expression[negate_index + 1]
        var = vars_values.get(var, var)
        expression[negate_index: negate_index + 2] = [int(not var)]
        return evaluate(expression, vars_values)

    func_dict = {'and': lambda a, b: a and b,
                  'or': lambda a, b: a or b,
                  '->': lambda a, b: not a or b,
                 '<->': lambda a, b: a == b}

    p, op, q = expression[:3]
    p, op, q = vars_values.get(p, p), func_dict[op], vars_values.get(q, q)
    expression[:3] = [int(op(p, q))]
    return evaluate(expression, vars_values)

def table_maker(*rows):
    """Generates an aligned table. https://github.com/salt-die/Table-Maker"""
    rows = list(rows)

    # Pad the length of items in each column
    lengths = list(map(len, rows[0]))
    for i, row in enumerate(rows):
        for j, (item, length) in enumerate(zip(row, lengths)):
            rows[i][j] = f'{item:^{length}}'

    # Construct table
    table = [f'│ {" │ ".join(row)} │' for row in rows]
    top, title, bottom = (f'{left}{mid.join("─" * (len(item) + 2) for item in rows[0])}{right}'
                          for left, mid, right in ('┌┬┐','├┼┤','└┴┘'))
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

    def pop(self, i):
        prop = self._props.pop(i)
        self._update_attributes()
        return prop

    def _update_attributes(self):
        self.expressions = [reformat(prop) for prop in self.props]
        self.vars = sorted(reduce(set.union, map(find_vars, self.expressions)))

        rows = generate(len(self.vars))

        self.table = []
        for values in rows:
            vars_values = {var:value for var, value in zip(self.vars, values)}
            results = [evaluate(expression, vars_values) for expression in self.expressions]
            self.table.append(values + results)

    def display(self, binary=False):
        translate = '01' if binary else 'FT'
        table = [[translate[value] for value in row] for row in self.table]
        table = table_maker(self.vars + self.props, *table)
        print(table)