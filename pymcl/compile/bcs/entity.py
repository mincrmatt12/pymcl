from pymcl.compile.bcs.bcs import LoadCommand
from pymcl.compile.bcs.stack import EntityPosition


class LoadEntityPosition(LoadCommand):
    def __init__(self, i, p_var: EntityPosition.PosVar):
        self.i = i
        self.p_var = p_var

    def get_load(self):
        return EntityPosition(self.i, self.p_var)
