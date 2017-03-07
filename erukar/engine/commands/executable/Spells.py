from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform
import erukar

class Spells(Command):
    aliases = ['spellbook', 'spells', 'my spells']

    def execute(self, *_):
        self.caster = self.find_player().lifeform()
        for eff in self.get_spells():
            self.append_result(self.sender_uid, eff)
        return self.succeed()

    def get_spells(self):
        for spell_word in self.server_properties.SpellWords:
            grasp = next((x for x in self.caster.spell_words if x.word_class == self.server_properties.SpellWords[spell_word]), None)
            if grasp is None:
                continue
            word = getattr(erukar.game.magic.words, grasp.word_class)
            yield '\n'.join([
                '"{}" -- {}'.format(spell_word, word.Name),
                '-'*16,
                'Proficiency:  {:3}%'.format(int(grasp.efficiency()*100)),
                word.Description + '\n',
            ])
