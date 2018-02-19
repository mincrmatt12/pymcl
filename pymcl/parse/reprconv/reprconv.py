from pymcl.parse import MCLParseError
from pymcl.parse.reprconv import exprconv, nameconv
from pymcl.repr import tree, stmt, functions, expr


def to_repr_function(clause):
    params = []
    returntype = nameconv.convert_type(clause.children[0].children[0])
    name = str(clause.children[0].children[1])
    if name == "print":
        raise MCLParseError('''you can't define a function called print''')
    for i in range(0, len(clause.children[1].children), 2):
        params.append(functions.Param(nameconv.convert_type(clause.children[1].children[i]),
                                      str(clause.children[1].children[i + 1])))
    return functions.Function(name, params, to_repr_stmt(clause.children[2]), returntype)


def to_repr_tree(parsetree):
    functions = []
    ns = ""

    for i in parsetree.children:  # start
        clause = i.children[0]  # toplevel_clause
        if clause.data == "namespace_clause":
            if ns == "":
                ns = str(clause.children[0])  # ident
            else:
                raise MCLParseError('''multiple namespace clauses''')
        elif clause.data == "function_clause":
            functions.append(to_repr_function(clause))

    if ns == "":
        raise MCLParseError('''no namespace clauses''')

    return tree.ParseTree(ns, functions)


def to_repr_stmt(parsestmt):
    parsestmt = parsestmt.children[0]
    if parsestmt.data == "expr_stmt":
        return stmt.ExprStmt(exprconv.convert_expr_node(parsestmt.children[0]))
    elif parsestmt.data == "assign_stmt":
        return stmt.AssignStmt(nameconv.convert_qual(parsestmt.children[0]),
                               exprconv.convert_expr_node(parsestmt.children[1]))
    elif parsestmt.data == "var_stmt":
        return stmt.VarStmt(nameconv.convert_type(parsestmt.children[0]), str(parsestmt.children[1]),
                            exprconv.convert_expr_node(parsestmt.children[2]) if len(parsestmt.children) == 3 else None)
    elif parsestmt.data == "block_stmt":
        return stmt.BlockStmt([to_repr_stmt(x) for x in parsestmt.children])
