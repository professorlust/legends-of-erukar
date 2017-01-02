from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
import random

class DamageOverTime(SpellEffect):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0
    DamageDuration = 4

    DamageDescription = "{alias|target} is consumed by a pulsing energy!"
    DamageShouldScale = False
    DamageName = 'nonelemental'
    DamageMod = 'acuity'

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of ice damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        
        self.append_for_all_in_room(self.mutate(self.DamageDescription))
        damages = [Damage(
            name=self.DamageName,
            damage_range=self.DamageRange, 
            mod=self.DamageMod,
            dist_and_params=(random.uniform, (0,1)),
            scales=self.DamageShouldScale
        )]
        dot_condition = erukar.game.conditions.negative.DamageOverTime(self.target, self.caster)
        dot_condition.duration = int(self.DamageDuration * efficacy)
        self.target.conditions.append(dot_condition)

        return parameters
