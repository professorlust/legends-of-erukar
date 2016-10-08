from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Cast(ActionCommand):
    NoSpell = "No spell '{}' was found in spell book."
    YouCastSpell = "You cast the spell '{}'."
    TheyCastSpell = "{} casts the spell '{}'."

    aliases = ['cast']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()
        payload = self.check_for_arguments()

        spell = self.find_spell(player, payload)
        if spell is None:
            return self.fail(self.NoSpell.format(payload))

        result = spell.on_cast(lifeform)
        self.append_result(self.sender_uid, self.YouCastSpell.format(spell.name))
        self.append_result(self.sender_uid, result)

        for content in lifeform.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not lifeform:
                self.append_result(content.uid, self.TheyCastSpell.format(lifeform.alias(), spell.name))
                self.append_result(content.uid, result)
        return self.succeed()

    def check_for_arguments(self):
        '''Stubbed for now'''
        return self.payload()
