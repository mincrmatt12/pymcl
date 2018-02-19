from pymcl.commands.command import CommandBase, add_suffix_function


class StoreLocal(CommandBase):
    def __init__(self, function, local, index_stack):
        self.function = function
        self.local = local
        self.index_stack = index_stack

    def get_commands(self):
        return [
            f"scoreboard players operation {self.local} {add_suffix_function(self.function, '_fLc')} = "
            f"s{self.index_stack} {add_suffix_function(self.function, '_fSk')}"
        ]


class LoadLocal(CommandBase):
    def __init__(self, function, local, index_stack):
        self.function = function
        self.local = local
        self.index_stack = index_stack

    def get_commands(self):
        return [
            f"scoreboard players operation s{self.index_stack} {add_suffix_function(self.function, '_fSk')} = "
            f"{self.local} {add_suffix_function(self.function, '_fLc')}"
        ]


class LoadConstant(CommandBase):
    def __init__(self, function, const, index_stack):
        self.function = function
        self.const = const
        self.index_stack = index_stack

    def get_commands(self):
        return [
            f"scoreboard players set s{self.index_stack} {add_suffix_function(self.function, '_fSk')} {self.const}"
        ]