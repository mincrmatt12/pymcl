import collections
import multiprocessing

from pymcl.commands.compiler.compiler import compile_bcs
from pymcl.commands.mcfunction import MCFunction
from pymcl.compile.compilers.stmtcompile import compile_stmt
from pymcl.compile.reqs import generate_setup_function_for_reqset
from pymcl.repr.tree import ParseTree


class CompileManager:
    def __init__(self, trees, start):
        self.parsetrees = trees
        self.functions = {}
        self.reqs = {}
        self.function_queue = multiprocessing.Queue()
        self.stdout_lock = multiprocessing.Lock()
        self.compile_tasks = multiprocessing.JoinableQueue()
        self.compile_tasks.put(start)
        self.setup_functions = []

    def compile(self, tree: ParseTree):
        # compile
        compiled_functions = {}

        ns = tree.ns
        for function in tree.functions:
            function.compute_locals()
            function.compute_recursive()

            function.ns = ns

            compile_stmt(function.bcs, function.code)
            function.commands = MCFunction(compile_bcs(function.bcs, function), ns + "__" + function.name)

            compiled_functions[ns + "::" + function.name] = function

        self.function_queue.put(compiled_functions)

    def run_worker(self):
        while not self.compile_tasks.empty():
            treename = self.compile_tasks.get()
            task = self.parsetrees[treename]
            with self.stdout_lock:
                print(f"Compiling {treename}")
            self.compile(task)
            self.compile_tasks.task_done()

    def run(self, workers=4):
        workers = min(workers, len(self.parsetrees))
        #processes = [multiprocessing.Process(target=CompileManager.run_worker, args=(self,)) for x in range(workers)]
        self.run_worker()
        self.compile_tasks.join()
        print("Generating setup")
        while not self.function_queue.empty():
            self.functions.update(self.function_queue.get())

        for i in self.functions:
            ns = self.functions[i].ns
            if ns not in self.reqs:
                self.reqs[ns] = []
            self.reqs[ns].extend(self.functions[i].get_requirements())

        for i in self.reqs:
            self.setup_functions.append(generate_setup_function_for_reqset(self.reqs[i], i))
