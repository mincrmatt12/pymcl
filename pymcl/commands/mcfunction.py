class MCFunction:
    def __init__(self, commands, name):
        self.commands = commands
        self.name = name

    def __iter__(self):
        return self.commands.__iter__()

    def get_content(self):
        c = []
        for i in self:
            c.extend(i.get_commands())
        return "\n".join(c)

    def get_fname(self):
        return self.name + ".mcfunction"
