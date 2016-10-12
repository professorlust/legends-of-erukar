from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ElectricDamage(SpellEffect):
    DamageRange = (0, 10)
    StandardCast = "{alias|target} is electrocuted!"

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of electric damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        self.target = self.get_target(lifeform, parameters)

        self.append_for_all_in_room(self.mutate(self.StandardCast))
        electric_damage = [Damage('electric', self.DamageRange, 'acuity',( random.uniform, (0,1)))]
        damages = [(x.roll(lifeform), 'electric') for x in electric_damage]
        self.cmd.inflict_damage(self.target, damages)
