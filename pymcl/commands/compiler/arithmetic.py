from pymcl.commands.stack.arithmetic import AddStack, SubStack, DivStack, MulStack, ModStack
from pymcl.compile.bcs import bcs as bcs_
from pymcl.compile.bcs.stack import MulStackItem


def compile_add(bcs_list, function, bcs: bcs_.Add, stack):
    if bcs.op == bcs_.AddStackItem.AddOp.ADD:
        return AddStack(function, len(stack)-2)
    else:
        return SubStack(function, len(stack) - 2)


def compile_mul(bcs_list, function, bcs: bcs_.Mul, stack):
    cls = {
        MulStackItem.MulOp.MUL: MulStack,
        MulStackItem.MulOp.DIV: DivStack,
        MulStackItem.MulOp.MOD: ModStack
    }
    return cls[bcs.op](function, len(stack) - 2)
