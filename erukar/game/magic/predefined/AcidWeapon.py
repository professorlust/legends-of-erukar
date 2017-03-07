from erukar.engine.magic.Spell import Spell
import erukar

class AcidWeapon(Spell):
    YouCastSpell = "You say a few words and touch your weapon. It instantly is consumed with a bubbling condensation that sizzles as it hits the ground!"
    TheyCastSpell = '{alias|caster} says some words and enchants his weapon with acid!'

    def __init__(self):
        super().__init__('Acid Weapon',[
            erukar.game.magic.effects.ElementalAcid(),
            erukar.game.magic.effects.AugmentWeapon()
        ])

