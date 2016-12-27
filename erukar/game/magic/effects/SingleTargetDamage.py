from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
import random

class SingleTargetDamage(SpellEffect):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0

    DamageDescription = "{alias|target} is hit with a blast of power!"
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
        self.target.apply_damage(damages, lifeform, efficacy)

        return parameters

    def get_rolled_damage(self, damage_type, lifeform, efficacy=1.0):
       raw = damage_type.roll(lifeform) * self.DamageScalar + self.DamageOffset
       return raw * efficacy
