import abc

from pymcl.commands.mcfunction import MCFunction


class CommandBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_commands(self):
        return []


def add_suffix_function(f: MCFunction, suffix):
    return f.name + suffix