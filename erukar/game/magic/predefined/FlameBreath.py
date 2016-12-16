from erukar.engine.model.Spell import Spell
import erukar

class FlameBreath(Spell):
    YouCastSpell = "You breathe in deeply, then exhale a large plume of flames from your lungs!"
    TheyCastSpell = '{alias|lifeform} breathes in deeply, then exhales a large plume of flames from {possessive_pronoun|lifeform} lungs!'

    def __init__(self):
        super().__init__('Flame Breath',[
            erukar.game.magic.effects.ElementalFire(),
            erukar.game.magic.effects.SingleTargetDamage()
        ])
