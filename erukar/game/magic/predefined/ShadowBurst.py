from erukar.engine.model.Spell import Spell
import erukar

class ShadowBurst(Spell):
    YouCastSpell = "You speak a few words in a demonic tongue, then raise your hands in the direction of {alias|target}. In the blink of an eye, a burst of dark energy escapes from your hand, twisting your stomach and crashing into your enemy."
    TheyCastSpell = "{alias|lifeform} raises his hands and speaks in a demonic tongue. Suddenly, a blast of dark energy collides with you, filling you with a terrible sense of despair!"

    def __init__(self):
        super().__init__('Shadow Burst',[
            erukar.game.magic.effects.ElementalDemonic(),
            erukar.game.magic.effects.ArcaneAdeptAugmentation(),
            erukar.game.magic.effects.SingleTargetDamage()
        ])

