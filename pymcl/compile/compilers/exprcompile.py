from pymcl.compile import MCLCompileError
from pymcl.compile.bcs.bcs import LoadConstant, LoadLocal, Add, Mul
from pymcl.compile.bcs.stack import AddStackItem, MulStackItem
from pymcl.repr.expr import IntConstant, StrConstant, AddExpr, Funccall, LocalExpr, MulExpr


def compile_add_expr(bcs_list, expr: AddExpr):
    add_bcs = Add(AddStackItem.AddOp.ADD if expr.op == AddExpr.AddOp.ADD else AddStackItem.AddOp.SUB)
    compile_expr(bcs_list, expr.right)
    compile_expr(bcs_list, expr.left)
    bcs_list.append(add_bcs)


def compile_mul_expr(bcs_list, expr):
    op = {
        MulExpr.MulOp.MUL: MulStackItem.MulOp.MUL,
        MulExpr.MulOp.DIV: MulStackItem.MulOp.DIV,
        MulExpr.MulOp.MOD: MulStackItem.MulOp.MOD,
    }
    compile_expr(bcs_list, expr.right)
    compile_expr(bcs_list, expr.left)
    bcs_list.append(Mul(op[expr.op]))


def compile_expr(bcs_list: list, expr):
    if type(expr) is IntConstant or (type(expr) != str and expr.is_constant()):
        bcs_list.append(LoadConstant(expr.constant_value()))
    elif type(expr) is LocalExpr:
        if "." in expr.target:
            raise NotImplementedError("haven't done full quals")
        bcs_list.append(LoadLocal(expr.target))
    elif type(expr) is StrConstant:
        raise MCLCompileError("you shouldn't be trying to compile a string")
    elif type(expr) is AddExpr:
        compile_add_expr(bcs_list, expr)
    elif type(expr) is MulExpr:
        compile_mul_expr(bcs_list, expr)
    elif type(expr) is Funccall:
        compile_funccall(bcs_list, expr)


# resolve circular crap
from pymcl.compile.compilers.funccallcompile import compile_funccall
