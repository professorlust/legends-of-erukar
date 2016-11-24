from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Use(ActionCommand):
    unlock = "{} successfully unlocked the {}!"

    aliases = ['use']
    TrackedParameters = ['item', 'target']

    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        # Get the object
        if 'object' in self.arguments:
            target = self.determine_target(player)

        for item in items:
            successful = item.on_use(self, target)
            if successful:
                self.dirty(player.lifeform())
                self.dirty(target)
                return self.succeed()

        return self.fail('Cannot use anything.')

    def check_for_arguments(self):
        # Copy all of the tracked Params into this command
        payload = self.user_specified_payload
        self.payloads = None

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

    def resolve_item(self, opt_payload=''):
        if self.context and self.context.should_resolve(self):
            self.item = getattr(self.context, 'item')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'item') and self.item: return

        return self.find_in_inventory(self.lifeform, opt_payload, 'item') 
