from erukar.engine.model.Spell import Spell
import erukar

class ElectricalBurst(Spell):
    YouCastSpell = "You speak a few words in ancient Canthric and raise your hands. Arcs of lightning and sparks fly from your fingertips towards {alias|target}!"
    TheyCastSpell = "{alias|caster} raises his hands and speaks in an ancient language. Suddenly, you are hit with bolts of lightning and sparks!"

    def __init__(self):
        super().__init__('Electrical Burst',[
            erukar.game.magic.effects.ElementalElectricity(),
            erukar.game.magic.effects.ArcaneAdeptAugmentation(),
            erukar.game.magic.effects.SingleTargetDamage()
        ])

