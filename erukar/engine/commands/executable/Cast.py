from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."

    aliases = ['cast']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()
        payload = self.check_for_arguments()

        spell = self.find_spell(lifeform, payload)
        if spell is None:
            return self.fail(self.NoSpell.format(payload))

        spell.on_cast(self, lifeform, self.arguments)
        return self.succeed()

    def check_for_arguments(self):
        '''Stubbed for now'''
        payload = self.payload()
        if ' on ' in payload:
            args = payload.split(' on ', 1)
            self.arguments['target'] = self.find_in_room(self.find_player().lifeform().current_room, args[1])
            return args[0]
        return payload
