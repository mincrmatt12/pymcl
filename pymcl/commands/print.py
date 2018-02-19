import json

from pymcl.commands.command import CommandBase, add_suffix_function
from pymcl.compile.bcs.bcs import PrintOutputGlobally


def format_json_text(text):
    return {
        "text": str(text)
    }


def format_json_score(score, name):
    return {
        "score": {
            "name": name,
            "objective": score
        }
    }


class PrintOutputGloballyCommand(CommandBase):
    class StackIndicator:
        def __init__(self, i):
            self.i = i

    def __init__(self, params, function, stack_index):
        self.params = params
        self.function = function
        self.stack_index = stack_index
        self.compute_stack_locations()

    def compute_stack_locations(self):
        j = 0
        for i in range(len(self.params)):
            if self.params[i] == PrintOutputGlobally.StackIndicator:
                self.params[i] = PrintOutputGloballyCommand.StackIndicator(self.stack_index + j)
                j += 1

    def get_commands(self):
        tellraw_components = []
        for i in self.params:
            if type(i) != PrintOutputGloballyCommand.StackIndicator:
                tellraw_components.append(format_json_text(i))
            else:
                tellraw_components.append(format_json_score(add_suffix_function(self.function, '_fSk'), f"s{i.i}"))
        return [
            f"tellraw @a {json.dumps(tellraw_components)}"
        ]
