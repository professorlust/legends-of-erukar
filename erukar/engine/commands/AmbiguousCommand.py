from erukar.engine.commands.Command import Command

class AmbiguousCommand(Command):
    def execute(self):
        if self.context is None or isinstance(self.context.context, type(self)):
            self.context = None
            return self.fail('Command is ambiguous.')
        print(self.context)

        new_cmd = type(self.context.context)()
        new_cmd.data = self.data
        new_cmd.context = self.context
        new_cmd.user_specified_payload = self.user_specified_payload
        new_cmd.sender_uid = self.sender_uid
        return new_cmd.execute()
