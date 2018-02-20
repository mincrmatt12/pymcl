from pymcl.compile.bcs.bcs import StoreLocal, StoreEntity, BcsList
from pymcl.compile.compilers.exprcompile import compile_expr
from pymcl.repr.stmt import ExprStmt, VarStmt, AssignStmt, BlockStmt


def compile_stmt(bcs_list: BcsList, stmt):
    extra_functions = {}
    if type(stmt) == ExprStmt:
        stmt: ExprStmt
        if stmt.has_side_effects():
            compile_expr(bcs_list, stmt.expr)
    elif type(stmt) == VarStmt:
        stmt: VarStmt
        if stmt.type_ == "int":
            compile_expr(bcs_list, stmt.expr)
            bcs_list.append(StoreLocal(stmt.assign_to))
        elif stmt.type_ == "entity":
            compile_expr(bcs_list, stmt.expr)
            bcs_list.entity_locals.append(stmt.assign_to)
            bcs_list.append(StoreEntity(bcs_list.entity_locals.index(stmt.assign_to)))
        bcs_list.local_types[stmt.assign_to] = stmt.type_
    elif type(stmt) == AssignStmt:
        compile_expr(bcs_list, stmt.expr)
        if bcs_list.local_types[stmt.stmt.assign_to] == "int":
            bcs_list.append(StoreLocal(stmt.assign_to))
        else:
            bcs_list.append(StoreEntity(bcs_list.entity_locals.index(stmt.assign_to)))
    elif type(stmt) == BlockStmt:
        stmt: BlockStmt
        for i in stmt.code:
            compile_stmt(bcs_list, i)
    return extra_functions
