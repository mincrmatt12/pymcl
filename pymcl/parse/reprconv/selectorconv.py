from typing import List

from pymcl.repr.expr import Expr
from pymcl.repr.selector import Selector, SelectCount, SelectType, SelectorClause, SelectDistance, SelectSort
from .exprconv import convert_expr_node
from ...parse import MCLParseError


def convert_compop_int_to_range(compop, int_: Expr):
    if not int_.is_constant():
        raise MCLParseError("gave non-constant value for range in selector")
    int_ = int_.constant_value()
    if type(int_) == int:
        if compop[0] == ">":
            min_val = int_ + 1 if not compop.endswith("=") else int_
            return min_val, None
        elif compop[0] == "<":
            min_val = int_ + 1 if not compop.endswith("=") else int_
            return None, min_val
        elif compop == "==":
            return int_, int_
        else:
            raise MCLParseError("gave != when range was expected")
    else:
        if compop != "==":
            raise MCLParseError("gave something other than == and range")
        return int_


def convert_select_attrib(attrib) -> SelectorClause:
    if attrib.children[0] == "dist":
        range_ = convert_compop_int_to_range(attrib.children[1], convert_expr_node(attrib.children[2]))
        return SelectDistance(*range_)


def convert_select_count(count):
    count_num = count.children[0]
    if count_num.type == "NUM":
        count_num = int(count_num)
    else:
        count_num = SelectCount.ANY
    if len(count.children) == 2:
        sort_type = {
            "random": SelectSort.RAND,
            "furthest": SelectSort.FAR,
            "nearest": SelectSort.NEAR,
            "arbitrary": SelectSort.ARB
        }[str(count.children[1])]
    else:
        sort_type = None
    r = [SelectCount(count_num)]
    if sort_type is not None:
        r.append(sort_type)
    return r


def convert_selector(selector_node):
    clauses: List[SelectorClause] = convert_select_count(selector_node.children[0])
    for child in selector_node.children[1:]:
        if child.data == "select_type":
            if len(child.children) == 2:
                clauses.append(SelectType(str(child.children[1]), True))
            else:
                clauses.append(SelectType(str(child.children[0]), False))
        else:
            for i in child.children:
                clauses.append(convert_select_attrib(i))

    s = Selector(clauses)
    return s
