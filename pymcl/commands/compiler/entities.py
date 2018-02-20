from pymcl.compile.bcs.stack import EntityReferenceStackItem


def get_selector_for_entityref(stackitem: EntityReferenceStackItem, function_):
    return f"@e[scores={{{function_.name + stackitem.get_table_name()}={stackitem.get_table_index()}}}]"
