from erukar.engine.model.Spell import Spell
import erukar

class Heal(Spell):
    YouCastSpell = 'You raise your arms in a beckoning prayer, casting {name}.'
    TheyCastSpell = '{alias|lifeform} raises {gender_pronoun_possessive|lifeform} arms in a beckoning prayer, casting {name}.'

    def __init__(self):
        super().__init__('Heal',[erukar.game.magic.effects.HealEffect()])
