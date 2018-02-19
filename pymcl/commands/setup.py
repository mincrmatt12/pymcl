from pymcl.commands.command import CommandBase


class SetupScoreboardCommand(CommandBase):
    def __init__(self, scoreboard):
        self.scoreboard = scoreboard

    def get_commands(self):
        return [f"scoreboard objectives add {self.scoreboard} dummy"]


