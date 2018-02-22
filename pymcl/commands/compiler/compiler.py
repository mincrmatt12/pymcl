from pymcl.commands.compiler.arithmetic import compile_add, compile_mul
from pymcl.commands.stack.entity import LoadLocalEntityPos
from pymcl.commands.stack.loadstore import LoadConstant, LoadLocal, StoreLocal, StoreEntityLocal, EvalSelectorCommand
from pymcl.commands.print import PrintOutputGloballyCommand, PrintOutputLocallyCommand
import pymcl.compile.bcs.bcs as bcs_
import pymcl.compile.bcs.entity as bcs_entity_


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
        elif type(bcs) == bcs_.StoreEntity:
            bcs: bcs_.StoreEntity
            commands.append(StoreEntityLocal(function, bcs.i, len(stack)-1, stack))
        elif type(bcs) == bcs_.EvalSelector:
            bcs: bcs_.EvalSelector
            commands.append(EvalSelectorCommand(function, bcs.sel_index, bcs.selector_text))
        elif type(bcs) == bcs_.Add:
            commands.append(compile_add(bcs_list, function, bcs, stack))
        elif type(bcs) == bcs_.Mul:
            commands.append(compile_mul(bcs_list, function, bcs, stack))
        elif type(bcs) == bcs_.PrintOutputGlobally:
            bcs: bcs_.PrintOutputGlobally
            commands.append(PrintOutputGloballyCommand(bcs.params, function, len(stack)-bcs.popcount()))
        elif type(bcs) == bcs_.PrintOutputLocally:
            bcs: bcs_.PrintOutputLocally
            commands.append(PrintOutputLocallyCommand(bcs.params, bcs.target, function, len(stack) - bcs.popcount()))
        elif type(bcs) == bcs_entity_.LoadEntityPosition:
            bcs: bcs_entity_.LoadEntityPosition
            commands.append(LoadLocalEntityPos(
                function, bcs.i, len(stack), bcs.p_var
            ))
        stack = bcs.apply_stack(stack)
    return commands
