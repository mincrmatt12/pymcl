from pymcl.commands.command import CommandBase, scoreboard_obsfucate


class SetupScoreboardCommand(CommandBase):
    def __init__(self, scoreboard):
        self.scoreboard = scoreboard

    def get_commands(self):
        return [f"scoreboard objectives add {scoreboard_obsfucate(self.scoreboard)} dummy"]


