from sly import Lexer, Parser
from .expressions import (
    Xor,
    Or,
    Iff,
    Implies,
    And,
    Negate,
    TRUE as TRUE_,
    FALSE as FALSE_,
    Var,
)


class LogicLexer(Lexer):
    tokens = { XOR, OR, IFF, IMPLIES, AND, TRUE, FALSE, NAME }
    ignore = ' '
    literals = { '~', '(', ')' }

    XOR = r'xor'
    OR = r'or'
    IFF = r'<->'
    IMPLIES = r'->'
    AND = r'and'
    NAME = r'[a-z]'

    @_(r'T')
    def TRUE(self, t):
        t.value = TRUE_
        return t

    @_(r'F')
    def FALSE(self, t):
        t.value = FALSE_
        return t

    @_(r'[a-z]')
    def NAME(self, t):
        t.value = Var(t.value)
        return t


class LogicParser(Parser):
    tokens = LogicLexer.tokens

    precedence = (
        ('left', XOR, OR, IFF, IMPLIES),
        ('left', AND),
        ('left', '(', ')'),
        ('right', '~')
    )

    lookup = {
        'xor': Xor,
        'or': Or,
        '<->': Iff,
        '->': Implies,
        'and': And
    }

    def __init__(self):
        self.vars = set()

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr XOR expr',
       'expr OR expr',
       'expr IFF expr',
       'expr IMPLIES expr',
       'expr AND expr',
    )
    def expr(self, p):
        return self.lookup[p[1]](p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"~" expr')
    def expr(self, p):
        return Negate(p.expr)

    @_('TRUE')
    def expr(self, p):
        return p.TRUE

    @_('FALSE')
    def expr(self, p):
        return p.FALSE

    @_('NAME')
    def expr(self, p):
        self.vars.add(p.NAME.name)
        return p.NAME
