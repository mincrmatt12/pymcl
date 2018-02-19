from pymcl.compile.compilemanager import CompileManager
from pymcl.parse.parsemanager import ParseManager, fname_to_rname

if __name__ == "__main__":
    in_file = "tests/hello.mcl"

    parsemanager = ParseManager(in_file)
    parsemanager.run()

    print("Parsed!")

    compilemanager = CompileManager(parsemanager.parsetrees, fname_to_rname(in_file, in_file))
    compilemanager.run()

    print("Compiled!")
    for func in compilemanager.functions:
        print(f"func: {func}")
        print(compilemanager.functions[func].commands.get_content())

    for func in compilemanager.setup_functions:
        print(f"func: {func.name}")
        print(func.get_content())