import lark

from ...repr import expr
from . import nameconv


def convert_add_expr_node(node):
    return expr.AddExpr(
        convert_expr_node(node.children[0]),
        convert_expr_node(node.children[2]),
        expr.AddExpr.AddOp.ADD if node.children[1] == "+" else expr.AddExpr.AddOp.SUB
    )


def convert_funccall_node(node):
    return expr.Funccall(nameconv.convert_qual_or_type(node.children[0]),
                         [convert_expr_node(x) for x in node.children[1].children])  # params


def convert_mul_expr_node(node):
    return expr.MulExpr(
        convert_expr_node(node.children[0]),
        convert_expr_node(node.children[2]),
        expr.MulExpr.MulOp.from_str(str(node.children[1]))
    )


def convert_expr_node(parse_expr):
    node = parse_expr.children[0]
    if node.data == "atom":
        return convert_atom_node(node)
    elif node.data == "expr":
        return convert_expr_node(node)
    elif node.data == "add_expr":
        return convert_add_expr_node(node)
    elif node.data == "mul_expr":
        return convert_mul_expr_node(node)
    elif node.data == "funccall":
        return convert_funccall_node(node)
    elif node.data == "selector":
        return convert_selector(node)


def convert_atom_node(atom):
    node = atom.children[0]
    if isinstance(node, lark.Tree):
        if node.data == "qual":
            return expr.LocalExpr(nameconv.convert_qual(node))
        elif node.data == "range":
            if len(node.children) == 1:
                return expr.Range(convert_expr_node(node.children[0]))
            else:
                return expr.Range(convert_expr_node(node.children[0]), convert_expr_node(node.children[1]))
        elif node.data == "r_range":
            return expr.Range(None, convert_expr_node(node.children[0]))
    elif node.type == "NUM":
        return expr.IntConstant(int(node))
    else:
        return expr.StrConstant(str(node)[1:-1])


from .selectorconv import convert_selector