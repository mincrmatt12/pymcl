from pymcl.commands.command import CommandBase, add_suffix_function
from pymcl.commands.compiler.entities import get_selector_for_entityref
from pymcl.compile.bcs.stack import EntityReferenceStackItem, LocalEntity, SelectorEntity


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


class StoreEntityLocal(CommandBase):
    def __init__(self, function, local_index, index_stack, stack):
        self.function = function
        self.local_index = local_index
        self.sitem: EntityReferenceStackItem = stack[index_stack]
        self.target = LocalEntity(self.local_index)

    def get_commands(self):
        return [
            f"scoreboard players set {get_selector_for_entityref(self.target, self.function)} "
            f"{add_suffix_function(self.function, '_fElc')} -1",
            f"scoreboard players set {get_selector_for_entityref(self.sitem, self.function, limit=1)} "
            f"{add_suffix_function(self.function, '_fElc')} {self.local_index}"
        ]


class EvalSelectorCommand(CommandBase):
    def __init__(self, function, selector_index, selector_text):
        self.function = function
        self.selector_index = selector_index
        self.selector_text = selector_text
        self.target = SelectorEntity(self.selector_index)

    def get_commands(self):
        return [
            f"scoreboard players set {get_selector_for_entityref(self.target, self.function)} "
            f"{add_suffix_function(self.function, '_fEls')} -1",
            f"scoreboard players set {self.selector_text} "
            f"{add_suffix_function(self.function, '_fEls')} {self.selector_index}"
        ]
