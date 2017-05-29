from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
import random, erukar

class Sunder(SpellWord):
    DamageRange = (0, 10)
    DamageScalar = 2.0
    DamageOffset = 10

    DamageDescription = "{alias|target} is covered in a dark orange light!"
    DamageShouldScale = False
    DamageName = 'nonelemental'
    DamageMod = 'acuity'
    MaterialClass = 'Metal'

    SpellWord = 'sunder'

    PotionName = 'Sundering'
    PotionPriceMultiplier = 0.4

    def on_cast(self, command, caster, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of ice damage to something, defaulting to the caster'''
        super().on_cast(command, caster, parameters)
        
        self.append_for_all_in_room(self.mutate(self.DamageDescription))
        damage = int((random.uniform(*self.DamageRange) * self.DamageScalar + self.DamageOffset) * efficacy)

        for item in self.applicable_items(command.target):
            self.append_for_all_in_room('{}\'s {} takes {} damage!'.format(command.target.alias(), item.alias(), damage))
            item.take_damage(damage)

        return parameters

    def applicable_items(self, target):
        material_class = getattr(erukar.game.modifiers.material.base, self.MaterialClass)
        for item in target.equipped_items():
            if isinstance(item.material, material_class):
                yield item
