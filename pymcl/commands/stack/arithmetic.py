from pymcl.commands.command import CommandBase, add_suffix_function


class AddStack(CommandBase):
    def __init__(self, function, stack_index):
        self.function = function
        self.stack_index = stack_index

    def get_commands(self):
        return [
            f"scoreboard players operation s{self.stack_index} {add_suffix_function(self.function, '_fSk')} += s"
            f"{self.stack_index+1} {add_suffix_function(self.function, '_fSk')}"
        ]


class SubStack(CommandBase):
    def __init__(self, function, stack_index):
        self.function = function
        self.stack_index = stack_index

    def get_commands(self):
        return [
            f"scoreboard players operation s{self.stack_index} {add_suffix_function(self.function, '_fSk')} >< s"
            f"{self.stack_index+1} {add_suffix_function(self.function, '_fSk')}",
            f"scoreboard players operation s{self.stack_index} {add_suffix_function(self.function, '_fSk')} -= s"
            f"{self.stack_index+1} {add_suffix_function(self.function, '_fSk')}"
        ]
