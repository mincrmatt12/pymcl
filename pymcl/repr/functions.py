from pymcl.compile.bcs.bcs import BcsList
from pymcl.compile.reqs import FunctionLocalRequirements, FunctionStackRequirements
from pymcl.repr.stmt import VarStmt, Stmt


class Param:
    def __init__(self, type_, name):
        self.type_ = type_
        self.name = name


class Function:
    def __init__(self, name, params, code: Stmt, returntype):
        self.params = params
        self.name = name
        self.locals = []
        self.entity_locals = []
        self.dependencies = []
        self.is_recursive = False
        self.code = code
        self.bcs = BcsList()
        self.commands = []
        self.returntype = returntype
        self.ns = ""

    def compute_locals(self):
        for stmt in self.code:
            if type(stmt) is VarStmt:
                stmt: VarStmt
                if stmt.type_ == "int":
                    self.locals.append(stmt.assign_to)
                elif stmt.type_ == "entity":
                    self.entity_locals.append(stmt.assign_to)

    def compute_recursive(self, functions):
        self.is_recursive = False # todo: recursion checking

    def get_requirements(self):
        return [FunctionLocalRequirements(self), FunctionStackRequirements(self)]
