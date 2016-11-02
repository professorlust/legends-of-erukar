from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."

    aliases = ['cast']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()
        payload, spell = self.check_for_arguments()

        if not spell:
            spell, failure_object = self.find_spell(lifeform, payload)
            if failure_object:
                return failure_object

        spell.on_cast(self, lifeform, self.arguments)
        return self.succeed()

    def check_for_arguments(self):
        '''Stubbed for now'''
        payload = self.payload()
        if isinstance(payload, erukar.engine.model.Spell):
            self.arguments = self.context.context.arguments
            return None, payload

        if ' on ' in payload:
            args = payload.split(' on ', 1)
            target, failure = self.find_in_room(self.find_player().lifeform().current_room, args[1])
            if not failure:
                self.arguments['target'] = target
            return args[0], None
        return payload, None
