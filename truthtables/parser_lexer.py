from sly import Lexer, Parser
from expressions import TRUE as _TRUE, FALSE as _FALSE, Var, Negate, And, Or, Implies, Iff, Xor


class LogicLexer(Lexer):
    tokens = {NAME, IFF, IMPLIES, AND, XOR, OR, TRUE, FALSE}
    ignore = ' '
    literals = { '~', '(', ')' }
    IFF = r'<->'; IMPLIES = r'->'; AND = r'and'; XOR = r'xor'; OR = r'or'; NAME = r'[a-z]'

    @_(r'T')
    def TRUE(self, t): t.value = _TRUE; return t

    @_(r'F')
    def FALSE(self, t): t.value = _FALSE; return t

    @_(r'[a-z]')
    def NAME(self, t): t.value = Var(t.value); return t


class LogicParser(Parser):
    tokens = LogicLexer.tokens
    precedence = (('left', OR, XOR, IFF, IMPLIES), ('left', AND), ('left', '(', ')'), ('right', '~'))
    lookup = {'or': Or, 'xor': Xor, '<->': Iff, '->': Implies, 'and': And}

    def __init__(self): self.vars = set()

    @_('expr')
    def statement(self, p): return p.expr

    @_('expr OR expr', 'expr XOR expr', 'expr IFF expr', 'expr IMPLIES expr', 'expr AND expr')
    def expr(self, p): return self.lookup[p[1]](p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p): return p.expr

    @_('"~" expr')
    def expr(self, p): return Negate(p.expr)

    @_('TRUE')
    def expr(self, p): return p.TRUE

    @_('FALSE')
    def expr(self, p): return p.FALSE

    @_('NAME')
    def expr(self, p): self.vars.add(p.NAME.name); return p.NAME
