from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
import erukar, random

class DamageOverTime(SpellWord):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0
    DamageDuration = 4
    DamageOverTimeEfficacy = 0.5

    DamageDescription = "{alias|target} is consumed by a pulsing energy!"
    DamageShouldScale = False
    DamageName = 'nonelemental'
    DamageMod = 'acuity'

    PotionName = 'Prolonged Poison'
    PotionPriceMultiplier = 5.0

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of ice damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        
        self.append_for_all_in_room(self.mutate(self.DamageDescription))
        dot_condition = erukar.game.conditions.negative.DamageOverTime(self.target, self.caster)
        dot_condition.damage = [Damage(
            name=self.DamageName,
            damage_range=self.DamageRange, 
            mod=self.DamageMod,
            dist_and_params=(random.uniform, (0,1)),
            scales=self.DamageShouldScale
        )]
        dot_condition.duration = int(self.DamageDuration * efficacy)
        dot_condition.damage_efficacy = self.DamageOverTimeEfficacy
        self.target.conditions.append(dot_condition)

        return parameters
