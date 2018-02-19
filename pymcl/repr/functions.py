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
        self.dependencies = []
        self.is_recursive = False
        self.code = code
        self.bcs = []
        self.commands = []
        self.returntype = returntype
        self.ns = ""

    def compute_locals(self):
        for stmt in self.code:
            if type(stmt) is VarStmt:
                self.locals.append(stmt.assign_to)

    def compute_recursive(self):
        self.is_recursive = False # todo: recursion checking

    def get_requirements(self):
        return [FunctionLocalRequirements(self), FunctionStackRequirements(self)]
