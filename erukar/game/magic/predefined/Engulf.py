from erukar.engine.model.Spell import Spell
import erukar

class Engulf(Spell):
    YouCastSpell = "Your acidic body swallows {alias|target}, engufing him!"
    TheyCastSpell = "{alias|caster} consumes {alias|target}, swallowing him and engulfing him in acid!"

    def __init__(self):
        super().__init__('Engulf',[
            erukar.game.magic.effects.ElementalAcid(),
            erukar.game.magic.effects.InflictConsumed(),
            erukar.game.magic.effects.DamageOverTime()
        ])

