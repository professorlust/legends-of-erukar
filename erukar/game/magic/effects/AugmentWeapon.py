from erukar.engine.model.SpellEffect import SpellEffect
from erukar.game.conditions.magical.AugmentedWeapon import AugmentedWeapon
import random

class AugmentWeapon(SpellEffect):
    StandardCast = "Glowing turquoise runes appear on the {EssentialPart|weapon} of {alias|lifeform}'s {alias|weapon}"
    FailedCast = "Embarrassingly, {alias|lifeform} seems to have forgotten to equip a weapon..."

    AugmentationType = 'Blessed'

    PotionName = 'Augmented Weapon'
    PotionPriceMultiplier = 7.5

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of fire damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)

        augment = AugmentedWeapon(self.target, self.AugmentationType)
        if augment.weapon is None:
            self.append_for_all_in_room(self.mutate(self.StandardCast,{'lifeform':self.target}))
            return

        self.weapon = augment.weapon
        self.target.conditions.append(augment)
        self.append_for_all_in_room(self.mutate(self.StandardCast,{'lifeform':self.target}))

        return parameters
