from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform
import erukar

class Spells(Command):
    aliases = ['spellbook', 'spells', 'my spells']

    def execute(self, *_):
        for eff in self.get_spells():
            self.append_result(self.sender_uid, eff)
        return self.succeed()

    def get_spells(self):
        for spell_word in self.server_properties.SpellWords:
            word_class = self.server_properties.SpellWords[spell_word]
            word = getattr(erukar.game.magic.effects, word_class)
            yield '\n'.join([
                '"{}" -- {}'.format(spell_word, word.Name),
                '-'*16,
                'Proficiency:  0.00',
                word.Description + '\n',
            ])
