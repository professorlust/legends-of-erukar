from erukar.engine.model.Spell import Spell
import erukar

class FireBurst(Spell):
    YouCastSpell = "You speak a few words in ancient Canthric and raise your hands towards {alias|target}, then a plume of superhot air and flame jets out at high speeds towards your target!"
    TheyCastSpell = "{alias|caster} raises his hands and speaks in an ancient language. Suddenly, you are hit with an incredibly hot blast of air and fire!"

    def __init__(self):
        super().__init__('Fire Burst',[
            erukar.game.magic.effects.ElementalFire(),
            erukar.game.magic.effects.ArcaneAdeptAugmentation(),
            erukar.game.magic.effects.DamageSingleTarget()
        ])

