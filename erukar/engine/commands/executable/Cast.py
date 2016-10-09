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

        spell = self.find_spell(player, payload)
        if spell is None:
            return self.fail(self.NoSpell.format(payload))

        spell.on_cast(self, lifeform)
        return self.succeed()

    def check_for_arguments(self):
        '''Stubbed for now'''
        return self.payload()
