from erukar.engine.magic.Spell import Spell
import erukar

class IceBurst(Spell):
    YouCastSpell = "You speak a few words in ancient Canthric, then raise your hands in the direction of {alias|target}. In a heartbeat, a wave of icicles, snow, and incredibly cold air jets out towards your target!"
    TheyCastSpell = "{alias|caster} raises his hands and speaks in an ancient language. Before you can react, a blast of freezing air, shards of ice, and snow hits you!"

    def __init__(self):
        super().__init__('Ice Burst',[
            erukar.game.magic.effects.ElementalIce(),
            erukar.game.magic.effects.ArcaneAdeptAugmentation(),
            erukar.game.magic.effects.DamageSingleTarget()
        ])

