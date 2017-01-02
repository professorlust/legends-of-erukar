from erukar.engine.model.Spell import Spell
import erukar

class AcidBreath(Spell):
    YouCastSpell = "You breathe in deeply, then exhale a large spray of corrosive acid!"
    TheyCastSpell = "{alias|caster} breathes in deeply, then exhales a large spray of corrosive acid!"

    def __init__(self):
        super().__init__('Acid Breath',[
            erukar.game.magic.effects.ElementalAcid(),
            erukar.game.magic.effects.DamageSingleTarget()
        ])
