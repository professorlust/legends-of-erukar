from ..Command import Command


class TickExecution(Command):
    NeedsArgs = False

    def execute(self):
        return self.succeed()
