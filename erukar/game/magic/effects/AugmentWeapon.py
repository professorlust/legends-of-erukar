from erukar.engine.model.SpellEffect import SpellEffect
from erukar.game.conditions.magical.AugmentedWeapon import AugmentedWeapon
import random

class AugmentWeapon(SpellEffect):
    StandardCast = "Glowing turquoise runes appear on the {EssentialPart|weapon} of {alias|lifeform}'s {alias|weapon}"
    FailedCast = "Embarrassingly, {alias|lifeform} seems to have forgotten to equip a weapon..."

    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'fire'

    PotionName = 'Augmented Weapon'
    PotionPriceMultiplier = 7.5

    Name = 'Augment Weapon'
    Description = 'Binds an effect to a weapon. Multiple weapons can be bound at higher proficiencies.'
    Flavor = 'A recent advancement in arcana, the "Augment Weapon" magic was developed at the Sidernes Academy in Luinden, Iuria as part of research conducted by Arcanist Felwin Bougarde. The research was based in part on pre-Theocracy battlemages whose legendary abilities to bind the elements to their items was once forgotten.'

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of fire damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)

        augment = AugmentedWeapon(self.target, self.AugmentationType, self.AugmentationSubclass)
        if augment.weapon is None:
            self.append_for_all_in_room(self.mutate(self.StandardCast,{'lifeform':self.target}))
            return

        self.weapon = augment.weapon
        self.target.conditions.append(augment)
        self.append_for_all_in_room(self.mutate(self.StandardCast,{'lifeform':self.target}))

        return parameters
