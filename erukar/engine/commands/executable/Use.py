from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Use(ActionCommand):
    unlock = "{} successfully unlocked the {}!"

    aliases = ['use']
    TrackedParameters = ['item', 'target']

    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        if isinstance(self.target, erukar.engine.model.Direction):
            door = self.room.get_in_direction(self.target)
            if door:
                self.target = door

        successful = self.item.on_use(self, self.target)
        if successful:
            self.dirty(self.lifeform)
            self.dirty(self.target)
            return self.succeed()
        return self.fail('asdf')

    def check_for_arguments(self):
        # Copy all of the tracked Params into this command
        payload = self.user_specified_payload
        self.payloads = None

        self.player = self.find_player()
        self.lifeform = self.player.lifeform()
        self.room = self.lifeform.current_room

        if self.context and self.context.requires_disambiguation and payload.isdigit():
            self.context.resolve_disambiguation(self.context.indexed_items[int(payload)-1])

        if self.context and hasattr(self.context.context, 'payloads') and self.context.context.payloads:
            self.payloads = getattr(self.context.context, 'payloads')

        if not self.payloads:
            if ' on ' in payload:
                self.payloads = payload.split(' on ', 1)
            else:
                self.payloads = (payload, self.sender_uid)

        fail = self.resolve_item(self.payloads[0])
        if fail: return fail

        fail = self.resolve_target(self.payloads[1])
        if fail: return fail

