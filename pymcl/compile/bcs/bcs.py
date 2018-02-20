import abc

from pymcl.compile.bcs.stack import IntConstantStackItem, LocalStackItem, AddStackItem, MulStackItem, StackItem, \
    LocalEntity, SelectorEntity


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
        return IntConstantStackItem(self.const)


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


class PrintOutputLocally(PrintOutputGlobally):
    def __init__(self, params, target):
        super().__init__(params)
        self.target = target

    def popcount(self):
        if self.target == self.StackIndicator:
            return super().popcount() + 1
        else:
            return super().popcount()


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


class Mul(Bytecode):
    def __init__(self, op: MulStackItem.MulOp):
        self.op = op

    def apply_stack(self, prev_stack):
        left = prev_stack[-1]
        right = prev_stack[-2]
        return prev_stack[:-2] + [MulStackItem(left, right, self.op)]


class LoadEntity(LoadCommand):
    def __init__(self, i):
        self.i = i

    def get_load(self):
        return LocalEntity(self.i)


class StoreEntity(StoreCommand):
    def __init__(self, i):
        self.i = i


class EvalSelector(LoadCommand):
    def __init__(self, sel_index, selector_text):
        self.sel_index = sel_index
        self.selector_text = selector_text

    def get_load(self):
        return SelectorEntity(self.sel_index)


class BcsList(list):
    def __init__(self):
        super().__init__()
        self.selector_alloc_count = 0
        self.uses_selectors = False
        self.stack_at = []

        self.local_types = {}
        self.entity_locals = []

    def new_selector(self):
        self.selector_alloc_count += 1
        self.uses_selectors = True
        return self.selector_alloc_count-1

    def stack_before(self, i):
        if i == 0:
            return []
        else:
            return self.stack_at[i-1]

    def append(self, o: Bytecode):
        self.stack_at.append(o.apply_stack(self.stack_before(len(self))))
        for i in self.stack_at[-1]:
            i: StackItem
            i.validate()
        super().append(o)
