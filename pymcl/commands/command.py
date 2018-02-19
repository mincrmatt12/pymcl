import abc

class CommandBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_commands(self):
        return []


def add_suffix_function(f, suffix):
    return f.ns + "__" + f.name + suffix