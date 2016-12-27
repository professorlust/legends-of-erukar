from erukar.engine.model.Spell import Spell
import erukar

class AcidBurst(Spell):
    YouCastSpell = "You speak a few words in ancient Canthric, raising your hands. Instantaneously, a billow of acid ruptures from your palms, dousing {alias|target}!" 
    TheyCastSpell = "{alias|caster} raises his hands and speaks in an ancient language. A billow of acid jettisons from his palms, and before you have a moment to respond it douses you completely!" 

    def __init__(self):
        super().__init__('Acid Burst',[
            erukar.game.magic.effects.ElementalAcid(),
            erukar.game.magic.effects.ArcaneAdeptAugmentation(),
            erukar.game.magic.effects.SingleTargetDamage()
        ])

