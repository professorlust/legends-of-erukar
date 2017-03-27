from erukar.engine.magic.MagicBase import MagicBase
from erukar.engine.magic.wordtypes import *

class Spell(MagicBase):
    YouCastSpell = "You cast '{name}'."
    TheyCastSpell = "{alias|lifeform} casts '{name}'."

    def __init__(self, name, effect_chain):
        self.name = name
        self.words = effect_chain

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        self.add_implied_words_where_valid()
        if not self.is_chain_valid(): return

        super().on_cast(command, lifeform, parameters, efficacy)

        self.append_result(lifeform.uid, self.mutate(self.YouCastSpell))
        self.append_for_others_in_room(self.mutate(self.TheyCastSpell))

        for eff in self.words:
            parameters = eff.on_cast(command, self.target, parameters, efficacy)

    def alias(self):
        return self.name

    def is_chain_valid(self):
        required_word_types = [ConversionWord, ShapeWord, SourceWord]
        return all(self.has_word_type(wt) for wt in required_word_types)

    def has_word_type(self, word_type):
        return any(isinstance(word, word_type) for word in self.words)

    def add_implied_words_where_valid(self):
#       if not self.has_word_type(ShapeWord):
#           self.words.append(TargetSelf())
#
#       if not self.has_word_type(ConversionWord):
#           self.words.append(UndefinedChaos())
        pass
