import abc
from typing import List

from pymcl.commands.mcfunction import MCFunction
from pymcl.commands.setup import SetupScoreboardCommand


class Requirements(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_scoreboards(self):
        pass


class FunctionLocalRequirements(Requirements):
    ENTFUNCNAME_PREFIX = "_fElc"
    ENTSFUNCNAME_PREFIX = "_fEsl"
    FUNCNAME_PREFIX = "_fLc"

    def __init__(self, func):
        self.func = func

    def get_scoreboards(self):
        begin = [
            self.func.ns + "__" + self.func.name + FunctionLocalRequirements.FUNCNAME_PREFIX] if self.func.locals else []

        if self.func.entity_locals is not []:
            begin.append(self.func.ns + "__" + self.func.name + FunctionLocalRequirements.ENTFUNCNAME_PREFIX)

        if self.func.bcs.uses_selectors:
            begin.append(self.func.ns + "__" + self.func.name + FunctionLocalRequirements.ENTSFUNCNAME_PREFIX)
        return begin


class FunctionStackRequirements(Requirements):
    FUNCNAME_PREFIX = "_fSk"

    def __init__(self, func):
        self.func = func

    def get_scoreboards(self):
        return [self.func.ns + "__" + self.func.name + FunctionStackRequirements.FUNCNAME_PREFIX]


def generate_setup_function_for_reqset(reqs: List[Requirements], ns):
    # todo: entities
    scoreboard_reqs = []
    for i in reqs:
        scoreboard_reqs.extend(i.get_scoreboards())
    commands = []
    for i in scoreboard_reqs:
        commands.append(SetupScoreboardCommand(i))
    return MCFunction(commands, f"{ns}_setup")