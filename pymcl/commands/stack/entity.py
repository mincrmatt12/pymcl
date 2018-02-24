from pymcl.commands.command import CommandBase, add_suffix_function
from pymcl.commands.compiler.entities import get_selector_for_entityref
from pymcl.compile.bcs.stack import EntityPosition, LocalEntity


class LoadLocalEntityPos(CommandBase):
    def __init__(self, function, local_i, index_stack, pvar):
        self.function = function
        self.i = local_i
        self.index_stack = index_stack
        self.p_var = {
            EntityPosition.PosVar.X: "[0]",
            EntityPosition.PosVar.Y: "[1]",
            EntityPosition.PosVar.Z: "[2]",
        }[pvar]

    def get_commands(self):
        return [
            f"execute store result score s{self.index_stack} {add_suffix_function(self.function, '_fSk')} run data"
            f" get entity {get_selector_for_entityref(LocalEntity(self.i), self.function, limit=True)} Pos{self.p_var}"
        ]
