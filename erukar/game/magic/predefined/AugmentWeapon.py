from erukar.engine.model.Spell import Spell
import erukar

class AugmentWeapon(Spell):
    YouCastSpell = 'You say a few words in ancient Canthric, "Iy azhi hiy luze", and touch your weapon.'
    TheyCastSpell = '{alias|lifeform} speaks some words in an ancient language, then touches {gender_pronoun_possessive|lifeform} weapon.'

    def __init__(self):
        super().__init__('Augment Weapon',[erukar.game.magic.effects.AugmentedWeaponEffect()])

