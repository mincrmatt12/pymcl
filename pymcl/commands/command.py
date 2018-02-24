import abc
import hashlib
from pymcl.commands.mcfunction import MCFunction


class CommandBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_commands(self):
        return []


def scoreboard_obsfucate(n):
    h = hashlib.new('sha256')
    h.update(bytes(n, encoding="utf-8"))
    return f"mcl_{h.hexdigest()}"[:15]


def add_suffix_function(f: MCFunction, suffix):
    return scoreboard_obsfucate(f.name + suffix)
