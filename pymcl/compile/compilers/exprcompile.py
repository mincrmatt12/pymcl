from pymcl.compile import MCLCompileError
from pymcl.compile.bcs.bcs import LoadConstant, LoadLocal, Add, Mul, BcsList, LoadEntity, EvalSelector
from pymcl.compile.bcs.stack import AddStackItem, MulStackItem
from pymcl.compile.compilers.entcompile import compile_ent_attr_lookup
from pymcl.repr.expr import IntConstant, StrConstant, AddExpr, Funccall, LocalExpr, MulExpr
from pymcl.repr.selector import Selector


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


def compile_expr(bcs_list: BcsList, expr):
    if type(expr) is IntConstant or (type(expr) != str and expr.is_constant()):
        bcs_list.append(LoadConstant(expr.constant_value()))
    elif type(expr) is LocalExpr:
        if "." in expr.target:
            qual_base = expr.target.split(".")[0]
            if qual_base not in bcs_list.local_types:
                raise MCLCompileError('''variable {} referenced before declaration'''.format(expr.target))
            elif bcs_list.local_types[qual_base] != "entity":
                raise NotImplementedError('''classes not done yet''')
            else:
                compile_ent_attr_lookup(bcs_list, expr.target)
                return
        elif expr.target not in bcs_list.local_types:
            raise MCLCompileError('''variable {} referenced before declaration'''.format(expr.target))
        elif bcs_list.local_types[expr.target] == "int":
            bcs_list.append(LoadLocal(expr.target))
        else:
            bcs_list.append(LoadEntity(bcs_list.entity_locals.index(expr.target)))
    elif type(expr) is StrConstant:
        raise MCLCompileError("you shouldn't be trying to compile a string")
    elif type(expr) is AddExpr:
        compile_add_expr(bcs_list, expr)
    elif type(expr) is MulExpr:
        compile_mul_expr(bcs_list, expr)
    elif type(expr) is Funccall:
        compile_funccall(bcs_list, expr)
    elif type(expr) is Selector:
        expr: Selector
        bcs_list.append(EvalSelector(bcs_list.new_selector(), expr.get_entire_selector()))


# resolve circular crap
from pymcl.compile.compilers.funccallcompile import compile_funccall
