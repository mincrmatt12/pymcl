from multiprocessing import JoinableQueue, Queue, Process
from pymcl.commands.compiler.compiler import compile_bcs
from pymcl.commands.mcfunction import MCFunction
from pymcl.compile.compilers.stmtcompile import compile_stmt
from pymcl.compile.reqs import generate_setup_function_for_reqset
from pymcl.datapack.datapack import Datapack
from pymcl.repr.tree import ParseTree
from collections import namedtuple

Queues = namedtuple("Queues", "compile_tasks function_queue extra_functions_queue parsetrees functions")


def resolve_function(functions, fname, parent_ns):
    if "::" not in fname:
        fname = parent_ns + "::" + fname
    return functions[fname]


class CompileManager:
    def __init__(self, trees, start):
        self.parsetrees = trees
        self.functions = {}
        self.reqs = {}
        self.function_queue = Queue()
        self.compile_tasks = JoinableQueue()
        self.extra_functions_queue = Queue()
        self.compile_tasks.put(start)
        self.extra_functions = []
        self.datapack = Datapack()

    @staticmethod
    def compile(queues, tree: ParseTree):
        compiled_functions = {}
        ns = tree.ns
        for function in tree.functions:
            function.compute_locals()
            function.compute_recursive(queues.functions)
            function.ns = ns
            extra_functions = compile_stmt(function.bcs, function.code)
            function.commands = MCFunction([], ns + "__" + function.name)
            function.commands.commands = compile_bcs(function.bcs, function.commands)
            for i in extra_functions:
                f = MCFunction([], i)
                f.commands = compile_bcs(extra_functions[i], f)
                queues.extra_functions_queue.put(f)

            compiled_functions[ns + "::" + function.name] = function
        queues.function_queue.put(compiled_functions)

    @staticmethod
    def run_worker(queues):
        while not queues.compile_tasks.empty():
            treename = queues.compile_tasks.get()
            task = queues.parsetrees[treename]
            print(f"Compiling {treename}")
            CompileManager.compile(queues, task)
            queues.compile_tasks.task_done()

    def run(self, workers=4):
        queues = Queues(self.compile_tasks, self.function_queue, self.extra_functions_queue, self.parsetrees,
                        self.functions.copy())

        p = [Process(name="compile_worker_{}".format(x), target=CompileManager.run_worker, args=(queues,)) for x in
             range(workers)]
        for i in p:
            i.start()
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
            self.extra_functions.append(generate_setup_function_for_reqset(self.reqs[i], i))

        print("Generating datapack files")
        for i in self.extra_functions:
            self.datapack.add_file(i)
        for func in self.functions.values():
            self.datapack.add_file(func.commands)
