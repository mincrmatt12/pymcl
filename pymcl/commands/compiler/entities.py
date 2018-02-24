from pymcl.commands.command import scoreboard_obsfucate
from pymcl.compile.bcs.stack import EntityReferenceStackItem


def get_selector_for_entityref(stackitem: EntityReferenceStackItem, function_, limit=False, type_=None):
    if not limit:
        s = f"@e[scores={{{scoreboard_obsfucate(function_.name + stackitem.get_table_name())}" \
            f"={stackitem.get_table_index()}}}"
    else:
        s = f"@e[scores={{{scoreboard_obsfucate(function_.name + stackitem.get_table_name())}=" \
            f"{stackitem.get_table_index()}}},limit=1"

    if type_ is not None:
        s += f",type={type_}"
    return s + "]"