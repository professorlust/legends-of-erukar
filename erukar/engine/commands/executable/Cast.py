from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."

    aliases = ['cast']
    TrackedParameters = ['spell', 'target']

    def execute(self):
        player = self.find_player()
        if player is None: return
        self.lifeform = player.lifeform()
        self.room = self.lifeform.current_room

        failure = self.check_for_arguments()
        if failure: return failure

        arguments = {'target': self.target}
        self.spell.on_cast(self, self.lifeform, arguments)
        return self.succeed()

    def resolve_spell(self, opt_payload=''):
        if self.context and self.context.should_resolve(self) and hasattr(self.context, 'spell'):
            self.spell = getattr(self.context, 'spell')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'spell') and self.spell: return

        return self.find_spell(self.lifeform, opt_payload, 'spell') 

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

        fail = self.resolve_spell(self.payloads[0])
        if fail: return fail

        fail = self.resolve_target(self.payloads[1])
        if fail: return fail
