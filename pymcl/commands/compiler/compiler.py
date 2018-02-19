from pymcl.commands.stack.arithmetic import AddStack, SubStack
from pymcl.commands.stack.loadstore import LoadConstant, LoadLocal, StoreLocal
from pymcl.commands.print import PrintOutputGloballyCommand
import pymcl.compile.bcs.bcs as bcs_


def compile_add(bcs_list, function, bcs: bcs_.Add, stack):
    if bcs.op == bcs_.AddStackItem.AddOp.ADD:
        return AddStack(function, len(stack)-2)
    else:
        return SubStack(function, len(stack) - 2)


def compile_bcs(bcs_list, function):
    commands = []
    stack = []
    for bcs in bcs_list:
        if type(bcs) == bcs_.LoadConstant:
            bcs: bcs_.LoadConstant
            commands.append(LoadConstant(function, bcs.const, len(stack)))
        elif type(bcs) == bcs_.LoadLocal:
            bcs: bcs_.LoadLocal
            commands.append(LoadLocal(function, bcs.local, len(stack)))
        elif type(bcs) == bcs_.StoreLocal:
            bcs: bcs_.StoreLocal
            commands.append(StoreLocal(function, bcs.local, len(stack)-1))
        elif type(bcs) == bcs_.Add:
            commands.append(compile_add(bcs_list, function, bcs, stack))
        elif type(bcs) == bcs_.PrintOutputGlobally:
            bcs: bcs_.PrintOutputGlobally
            commands.append(PrintOutputGloballyCommand(bcs.params, function, len(stack)-bcs.popcount()))
        stack = bcs.apply_stack(stack)
    return commands