"""Idea taken from "Coding Trees in Python": https://www.youtube.com/watch?v=7tCNu4CnjVc"""


class Expr:
    pass


class Op(Expr):
    def __init__(self, op, func):
        self.op = op
        self.func = func


class UnOp(Op):
    """Unary Operator"""
    def __init__(self, op, func, expr):
        super().__init__(op, func)
        self.expr = expr

    def __repr__(self):
        if isinstance(self.expr, BinOp):
            return f'{self.op}({self.expr})'
        return f'{self.op}{self.expr}'

    def __call__(self, **var_values):
        return self.func(self.expr(**var_values))


class BinOp(Op):
    """Binary Operator"""
    def __init__(self, op, func, left, right):
        super().__init__(op, func)
        self.l = left
        self.r = right

    def __repr__(self):
        left = f'({self.l})' if isinstance(self.l, BinOp) else f'{self.l}'
        right = f'({self.r})' if isinstance(self.r, BinOp) else f'{self.r}'
        return f'{left} {self.op} {right}'

    def __call__(self, **var_values):
        return self.func(self.l(**var_values), self.r(**var_values))


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __call__(self, **var_values):
        return var_values[self.name]


class Const(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __call__(self, **var_values):
        return self.value


class TRUE(Const):
    def __init__(self):
        super().__init__(True)

    def __repr__(self):
        return 'T'


class FALSE(Const):
    def __init__(self):
        super().__init__(False)

    def __repr__(self):
        return 'F'


class Negate(UnOp):
    def __init__(self, p):
        super().__init__('~', lambda p:not p, p)


class And(BinOp):
    def __init__(self, p, q):
        super().__init__('and', lambda p, q:p and q, p, q)


class Or(BinOp):
    def __init__(self, p, q):
        super().__init__('or', lambda p, q:p or q, p, q)


class Implies(BinOp):
    def __init__(self, p, q):
        super().__init__('->', lambda p, q:not p or q, p, q)


class Iff(BinOp):
    def __init__(self, p, q):
        super().__init__('<->', lambda p, q:p == q, p, q)


class Xor(BinOp):
    def __init__(self, p, q):
        super().__init__('xor', lambda p, q:p != q, p, q)
