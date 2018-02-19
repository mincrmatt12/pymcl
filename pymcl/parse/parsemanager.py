import lark

from pymcl.parse import MCLParseError
from pymcl.parse.reprconv import reprconv
from .grammar import parser
import queue
import os


def fname_to_rname(fname, f_from):
    p = os.path.relpath(fname, os.path.split(f_from)[0])
    p = os.path.splitext(p)[0]
    p = os.path.normcase(p)
    p = p.lower()
    p = p.split(os.pathsep)
    return ".".join(p)


class ParseManager:
    def __init__(self, root_file):
        self.root_file = root_file
        self.to_parse = queue.Queue()
        self.to_parse.put((self.root_file, self.root_file))
        self.parsetrees = {}

    def run(self):
        while not self.to_parse.empty():
            p = self.to_parse.get()
            with open(p[0], "r") as f:
                try:
                    print(f"Parsing {p[0]}")
                    tree: lark.Tree = parser.parse(f.read())
                    print(f"Repring {p[0]}")
                    tree = reprconv.to_repr_tree(tree)
                    # todo: find imports
                    self.parsetrees[fname_to_rname(*p)] = tree
                except lark.ParseError as e:
                    raise MCLParseError(f"Parse error while parsing {p[0]}: \n{e}")

    def get_parsetrees(self):
        return self.parsetrees

