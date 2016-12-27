from erukar.engine.model.Spell import Spell
import erukar

class Heal(Spell):
    YouCastSpell = 'You raise your arms in a beckoning prayer, casting {name}.'
    TheyCastSpell = '{alias|caster} raises {possessive_pronoun|caster} arms in a beckoning prayer, casting {name}.'

    def __init__(self):
        super().__init__('Heal',[erukar.game.magic.effects.HealEffect()])
