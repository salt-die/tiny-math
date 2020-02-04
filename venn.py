"""
a b c a b c
| | | | | |
a | | | | |
 a&b| | | |
  a&b&c | |
     b&c| |
        c |
          ∅
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
