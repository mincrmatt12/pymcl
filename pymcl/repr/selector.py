import enum
from typing import List

from pymcl.repr.expr import Expr


class SelectorClause:
    def to_selector_clause(self):
        return ""


class SelectCount(SelectorClause):
    ANY = None

    def __init__(self, count):
        self.count = count

    def to_selector_clause(self):
        return f"limit={self.count}" if self.count != SelectCount.ANY else ""


class SelectSort(enum.Enum, SelectorClause):
    FAR = "furthest"
    NEAR = "nearest"
    RAND = "random"
    ARB = "arbitrary"

    def to_selector_clause(self):
        return f"sort={self.value}"


class SelectDistance(SelectorClause):
    def __init__(self, min_d, max_d):
        self.min_d = min_d
        self.max_d = max_d

    def to_selector_clause(self):
        min_d = self.min_d if self.min_d is not None else ""
        max_d = self.max_d if self.max_d is not None else ""
        return f"distance={min_d}..{max_d}"


class SelectType(SelectorClause):
    def __init__(self, type_, negated):
        self.type_ = type_
        self.negated = negated

    def to_selector_clause(self):
        neg_s = {True: "!=", False: "="}[self.negated]
        return f"type{neg_s}{self.type_}"


class Selector(Expr):
    def __init__(self, clauses: List[SelectorClause]):
        self.clauses = clauses

    def get_entire_selector(self):
        return f"@e[{','.join((x.to_selector_clause() for x in self.clauses))}]"
