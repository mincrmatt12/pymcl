import enum
from typing import Optional
import operator


class Expr:
    def is_constant(self):
        return False

    def constant_value(self):
        return None


class Constant(Expr):
    def is_constant(self):
        return True

    def __str__(self):
        return f"{self.__class__.__name__}, value {self.constant_value()}"


class IntConstant(Constant):
    def __init__(self, int_value):
        self.int_value = int_value

    def constant_value(self):
        return self.int_value


class StrConstant(Constant):
    def __init__(self, str_value):
        self.str_value = str_value

    def constant_value(self):
        return self.str_value


class AddExpr(Expr):
    class AddOp(enum.Enum):
        ADD = 1
        SUB = 2

    def __init__(self, left: Expr, right: Expr, op: AddOp):
        self.left = left
        self.right = right
        self.op = op

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def constant_value(self):
        return self.left.constant_value() + self.right.constant_value() if self.op == AddExpr.AddOp.ADD else \
            self.left.constant_value() - self.right.constant_value()


class MulExpr(Expr):
    class MulOp(enum.Enum):
        MUL = operator.mul
        DIV = operator.floordiv
        MOD = operator.mod

        @staticmethod
        def from_str(s):
            return {
                "*": MulExpr.MulOp.MUL,
                "/": MulExpr.MulOp.DIV,
                "%": MulExpr.MulOp.DIV
            }[s]

    def __init__(self, left: Expr, right: Expr, op: MulOp):
        self.left = left
        self.right = right
        self.op = op

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def constant_value(self):
        # noinspection PyCallingNonCallable
        return self.op(self.left.constant_value(), self.right.constant_value())


class Funccall(Expr):
    def __init__(self, target, params):
        self.target = target
        self.params = params


class LocalExpr(Expr):
    def __init__(self, target):
        self.target = target


class Range(Expr):
    def __init__(self, min: Optional[Expr] = None, max: Optional[Expr] = None):
        self.min = min
        self.max = max

    def is_constant(self):
        return (self.min.is_constant() if self.min is not None else True) and (
            self.max.is_constant() if self.max is not None else True)

    def constant_value(self):
        return [self.min.constant_value() if self.min is not None else None,
                self.max.constant_value() if self.max is not None else None]
