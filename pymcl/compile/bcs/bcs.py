import abc

from pymcl.compile.bcs.stack import IntStackItem, LocalStackItem, AddStackItem


class Bytecode:
    def apply_stack(self, prev_stack):
        return prev_stack


class LoadCommand(Bytecode, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_load(self):
        pass

    def apply_stack(self, prev_stack):
        return prev_stack + [self.get_load()]


class StoreCommand(Bytecode):
    def apply_stack(self, prev_stack):
        return prev_stack[:-1]


class LoadConstant(LoadCommand):
    def __init__(self, const):
        self.const = const

    def get_load(self):
        return IntStackItem(self.const)


class LoadLocal(LoadCommand):
    def __init__(self, local):
        self.local = local

    def get_load(self):
        return LocalStackItem(self.local)


class PrintOutputGlobally(Bytecode):
    class StackIndicator:
        pass

    def __init__(self, params):
        self.params = params

    def popcount(self):
        return sum((int(x == PrintOutputGlobally.StackIndicator) for x in self.params))

    def apply_stack(self, prev_stack):
        popcount = self.popcount()
        return prev_stack[:-popcount]


class StoreLocal(StoreCommand):
    def __init__(self, local):
        self.local = local


class Add(Bytecode):
    def __init__(self, op: AddStackItem.AddOp):
        self.op = op

    def apply_stack(self, prev_stack):
        left = prev_stack[-1]
        right = prev_stack[-2]
        return prev_stack[:-2] + [AddStackItem(left, right, self.op)]
