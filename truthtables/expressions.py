class Expr:
    pass

class Op(Expr):
    def __init__(self, op, func):
        self.op = op
        self.func = func

class UnOp(Op):
    """Unary Operator"""
    def __init__(self, op, func, val):
        super().__init__(op, func)
        self.val = val

    def __repr__(self):
        return f'{self.op}{self.val}'

    def __call__(self, **var_values):
        return self.func(self.val(**var_values))

class BinOp(Op):
    """Binary Operator"""
    def __init__(self, op, func, left, right):
        super().__init__(op, func)
        self.left = left
        self.right = right

    def __repr__(self):
        left = f'({self.left})' if isinstance(self.left, BinOp) else f'{self.left}'
        right = f'({self.right})' if isinstance(self.right, BinOp) else f'{self.right}'
        return f'{left} {self.op} {right}'

    def __call__(self, **var_values):
        return self.func(self.left(**var_values), self.right(**var_values))

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