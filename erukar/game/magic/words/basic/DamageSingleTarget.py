from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
from erukar.engine.formatters.MagicDamageFormatter import MagicDamageFormatter
import random

class DamageSingleTarget(SpellWord):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0

    DamageDescription = "{alias|target} is hit with a blast of power!"
    DamageShouldScale = False
    DamageName = 'nonelemental'
    DamageMod = 'acuity'

    PotionName = 'Instant Poison'
    PotionPriceMultiplier = 5.0

    def on_cast(self, command, caster, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of ice damage to something, defaulting to the caster'''
        super().on_cast(command, caster, parameters)
        
        self.append_for_all_in_room(self.mutate(self.DamageDescription))
        damages = [Damage(
            name=self.DamageName,
            damage_range=self.DamageRange, 
            mod=self.DamageMod,
            dist_and_params=(random.uniform, (0,1)),
            scales=self.DamageShouldScale
        )]
        result = self.target.apply_damage(damages, caster, efficacy)
        MagicDamageFormatter.process_and_append_damage_result(command, result)

        return parameters
