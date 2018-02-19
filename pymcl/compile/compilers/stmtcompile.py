from pymcl.compile.bcs.bcs import StoreLocal
from pymcl.compile.compilers.exprcompile import compile_expr
from pymcl.repr.stmt import ExprStmt, VarStmt, AssignStmt, BlockStmt


def compile_stmt(bcs_list, stmt):
    if type(stmt) == ExprStmt:
        stmt: ExprStmt
        if stmt.has_side_effects():
            compile_expr(bcs_list, stmt.expr)
    elif type(stmt) == VarStmt:
        stmt: VarStmt
        if stmt.type_ != "int":
            raise NotImplementedError("todo: typing") # todo
        compile_expr(bcs_list, stmt.expr)
        bcs_list.append(StoreLocal(stmt.assign_to))
    elif type(stmt) == AssignStmt:
        compile_expr(bcs_list, stmt.expr)
        bcs_list.append(StoreLocal(stmt.assign_to))
    elif type(stmt) == BlockStmt:
        stmt: BlockStmt
        for i in stmt.code:
            compile_stmt(bcs_list, i)
