from erukar.engine.model.Spell import Spell
import erukar

class Heal(Spell):
    Description = '{alias|lifeform} raises {gender_pronoun_possessive|lifeform} arms in a beckoning prayer.'

    def __init__(self):
        super().__init__('Heal',self.Description,[erukar.game.magic.effects.HealEffect()])
