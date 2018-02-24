
import queue

from pymcl.commands.compiler.compiler import compile_bcs
from pymcl.commands.mcfunction import MCFunction
from pymcl.compile.compilers.stmtcompile import compile_stmt
from pymcl.compile.reqs import generate_setup_function_for_reqset
from pymcl.datapack.datapack import Datapack
from pymcl.repr.tree import ParseTree


class CompileManager:
    def __init__(self, trees, start):
        self.parsetrees = trees
        self.functions = {}
        self.reqs = {}
        self.function_queue = queue.Queue()
        self.compile_tasks = queue.Queue()
        self.compile_tasks.put(start)
        self.extra_functions = []
        self.datapack = Datapack()

    def compile(self, tree: ParseTree):
        compiled_functions = {}
        ns = tree.ns
        for function in tree.functions:
            function.compute_locals()
            function.compute_recursive()
            function.ns = ns
            extra_functions = compile_stmt(function.bcs, function.code)
            function.commands = MCFunction([], ns + "__" + function.name)
            function.commands.commands = compile_bcs(function.bcs, function.commands)
            for i in extra_functions:
                f = MCFunction([], i)
                f.commands = compile_bcs(extra_functions[i], f)
                self.extra_functions.append(f)

            compiled_functions[ns + "::" + function.name] = function
        self.function_queue.put(compiled_functions)

    def run_worker(self):
        while not self.compile_tasks.empty():
            treename = self.compile_tasks.get()
            task = self.parsetrees[treename]
            print(f"Compiling {treename}")
            self.compile(task)
            self.compile_tasks.task_done()

    def run(self):
        self.run_worker()
        print("Generating setup")

        while not self.function_queue.empty():
            self.functions.update(self.function_queue.get())
        for i in self.functions:
            ns = self.functions[i].ns
            if ns not in self.reqs:
                self.reqs[ns] = []
            self.reqs[ns].extend(self.functions[i].get_requirements())
        for i in self.reqs:
            self.extra_functions.append(generate_setup_function_for_reqset(self.reqs[i], i))

        print("Generating datapack files")
        for i in self.extra_functions:
            self.datapack.add_file(i)
        for func in self.functions.values():
            self.datapack.add_file(func.commands)
