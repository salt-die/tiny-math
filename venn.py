"""
A simple implementaion of one-dimensional venn diagrams.

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
|      |------------|   |
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
