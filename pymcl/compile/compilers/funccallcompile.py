from typing import List, Union

from pymcl.compile.bcs.bcs import PrintOutputGlobally
from pymcl.repr.expr import Funccall, Expr, StrConstant
from .exprcompile import compile_expr


def get_print_args(bcs_list, params: List[Union[str, Expr]]):
    print_args = []
    for i in params:
        if type(i) == str:
            compile_expr(bcs_list, i)
            print_args.append(PrintOutputGlobally.StackIndicator)
        elif i.is_constant():
            i: Expr
            print_args.append(i.constant_value())
        else:
            compile_expr(bcs_list, i)
            print_args.append(PrintOutputGlobally.StackIndicator)
    return print_args


def compile_print(bcs_list, expr: Funccall):
    if not expr.params:
        return
    if False:
        pass  # todo: entity check
    else:
        bcs_list.append(PrintOutputGlobally(get_print_args(bcs_list, expr.params)))


def compile_funccall(bcs_list, expr: Funccall):
    if expr.target == "print":
        compile_print(bcs_list, expr)
    else:
        pass  # todo
