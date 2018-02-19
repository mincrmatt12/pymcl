import abc
from typing import List

from .expr import Expr


class Stmt:
    def stmt_list(self):
        return [self]

    def __iter__(self):
        return self.stmt_list().__iter__()

    pass  # base class


class AssignStmt(Stmt):
    def __init__(self, assign_to, expr: Expr):
        self.assign_to = assign_to
        self.expr = expr

    def is_constant(self):
        return self.expr.is_constant()

    def constant_value(self):
        return self.expr.constant_value()


class VarStmt(AssignStmt):
    def __init__(self, type_, assign_to, expr: Expr = None):
        super().__init__(assign_to, expr)
        self.type_ = type_

    def is_constant(self):
        return True if not self.has_value() else super().is_constant()

    def constant_value(self):
        return super().constant_value() if self.has_value() else None

    def has_value(self):
        return self.expr is not None


class ExprStmt(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def has_side_effects(self):
        return True  # todo


class BlockStmt(Stmt):
    def __init__(self, code: List[Stmt]):
        self.code = code

    def stmt_list(self):
        stmts = []
        for i in self.code:
            stmts.extend(i.stmt_list())
        return stmts
