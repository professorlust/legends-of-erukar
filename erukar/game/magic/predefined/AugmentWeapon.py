from erukar.engine.model.Spell import Spell
import erukar

class AugmentWeapon(Spell):
    YouCastSpell = 'You say a few words in ancient Canthric, "Iy azhi hiy luze", and touch your weapon.'
    TheyCastSpell = '{alias|caster} speaks some words in an ancient language, then touches {possessive_pronoun|caster} weapon.'

    def __init__(self):
        super().__init__('Augment Weapon',[erukar.game.magic.effects.AugmentedWeaponEffect()])

