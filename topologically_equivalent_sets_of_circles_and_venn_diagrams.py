"""
Here's an attempt at generating topologically equivalent sets of non-intersecting circles with a
simple grammar.

Example:
In [159]: set(all_words_length(3))
Out[159]: {((())), (()()), (())(), ()(()), ()()()}

Unfortunately (())() is really the same as ()(()) so we're not quite there.
"""
class Word:
    def __init__(self, word1=None, word2=None, concat=True):
        if word1 is None:
            self.word = '()'
        elif concat:
            self.word = f'{word1.word}{word2.word}'
        else:
            self.word = f'{word1.word[0]}{word2.word}{word1.word[1:]}'

    def __repr__(self):
        return self.word

    def __add__(self, other):
        return Word(self, other)

    def __rshift__(self, other):
        return Word(self, other, concat=False)

    def __eq__(self, other):
        return self.word == other.word

    def __hash__(self):
        return hash(self.word)


def all_words_length(n):
    if n == 1:
        yield Word()
        return
    for word in all_words_length(n - 1):
        yield word + Word()
        yield Word() + word
        yield word >> Word()
        yield Word() >> word
"""
We can improve using partitions though probably, a task for another day:
def partitions(n, m=None):
    if m is None or m >= n:
        yield [n]
        start = n - 1
    else:
        start = m

    for m0 in range(start, 0, -1):
        for subpartition in partitions(n - m0, m0):
            yield [m0] + subpartition
"""



"""
We can also try to generate topologically equivalent sets of intersecting circles, but we reach some
limitations of our 1-d representation and we also once again produce some redundant sets:

In [168]: [*possibles()]
Out[168]:
['()[]{}',
 '()[{]}',
 '()[{}]',
 '([)]{}',
 '([){]}',
 '([){}]',
 '([]){}',
 '([]{)}',
 '([]{})',
 '([{)]}',
 '([{)}]',
 '([{])}',
 '([{]})',
 '([{})]',
 '([{}])']
"""

required = {'[':'(', '{':'[', ')':'(', ']':'[', '}':'{'}

def possibles(current=('(',), brackets_left=(')', '[', ']', '{', '}')):
    if not brackets_left:
        yield ''.join(current)
        return

    for bracket in brackets_left:
        if required[bracket] in current:
            brackets = tuple(filter(bracket.__ne__, brackets_left))
            yield from possibles(current + (bracket,), brackets)

"""
Intersecting circles are similar to Venn diagrams, but venn diagrams can produce intersections that
aren't possible with just circles:

A simple implementation of one-dimensional venn diagrams.

Examples:
    In [220]: Venn('abcabc')
    Out[220]: ∅, a&c&b, a&b, a, c, c&b

    In [221]: Venn('ab')
    Out[221]: a&b, a

    In [222]: Venn('abac')
    Out[222]: a&b, a, b, c&b

This works by incrementally removing a set if it exists else adding it:
    a b c a b c
    | | | | | |
    a | | | | |
     a&b| | | |
      a&b&c | |
         b&c| |
            c |
              ∅

    This describes the venn diagram:
+-----------------------+
|                       |
|                       |
|A                      |
|      +------------+   |
|      |            |   |
|  +------------------+ |
|  |   |            | | |
+-----------------------+
   |   |B           | |
   |C  |            | |
   |   |            | |
   |   +------------+ |
   |                  |
   |                  |
   |                  |
   +------------------+
"""
class Venn:
    def __init__(self, venn):
        self.__make__(venn)

    def __make__(self, venn):
        relations = set()
        s = set()
        for symbol in venn:
             (set.remove if symbol in s else set.add)(s, symbol)
             relations.add("&".join(s) if s else "∅")
        self.__rep__ = ", ".join(relations)

    def __repr__(self):
        return self.__rep__
