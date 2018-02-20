import enum

from pymcl.compile import MCLCompileError


class StackItem:
    def is_constant(self):
        return False

    def constant_value(self):
        return None

    def validate(self):
        pass


class IntStackItem(StackItem):
    pass


class IntConstantStackItem(IntStackItem):
    def __init__(self, val):
        self.val = val

    def is_constant(self):
        return True

    def constant_value(self):
        return self.val


class LocalStackItem(IntStackItem):
    def __init__(self, local):
        self.local = local


class AddStackItem(IntStackItem):
    class AddOp(enum.Enum):
        ADD = 1
        SUB = 2

    def __init__(self, left: IntStackItem, right: IntStackItem, op: AddOp):
        self.left = left
        self.right = right
        self.op = op

    def validate(self):
        if not (issubclass(self.left.__class__, IntStackItem) and issubclass(self.right.__class__, IntStackItem)):
            raise MCLCompileError('''add called on two non-int exprs''')

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def constant_value(self):
        return self.left.constant_value() + self.right.constant_value() if self.op == AddStackItem.AddOp.ADD else \
            self.left.constant_value() - self.right.constant_value()


class MulStackItem(IntStackItem):
    class MulOp(enum.Enum):
        MUL = lambda x, y: x * y
        DIV = lambda x, y: x // y
        MOD = lambda x, y: x % y

    def __init__(self, left: IntConstantStackItem, right: IntConstantStackItem, op: MulOp):
        self.left = left
        self.right = right
        self.op = op

    def is_valid(self):
        if not issubclass(self.left.__class__, IntStackItem) and issubclass(self.right.__class__, IntStackItem):
            raise MCLCompileError('''mul called on two non-int exprs''')

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def constant_value(self):
        return self.op(self.left.constant_value(), self.right.constant_value())


class EntityReferenceStackItem(StackItem):
    def get_table_name(self):
        pass

    def get_table_index(self):
        pass


class LocalEntity(EntityReferenceStackItem):
    def __init__(self, local_index):
        self.local_index = local_index

    def get_table_name(self):
        return "_fElc"

    def get_table_index(self):
        return self.local_index


class SelectorEntity(EntityReferenceStackItem):
    def __init__(self, local_index):
        self.local_index = local_index

    def get_table_name(self):
        return "_fEsl"

    def get_table_index(self):
        return self.local_index
