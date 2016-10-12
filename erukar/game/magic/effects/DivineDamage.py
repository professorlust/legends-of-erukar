from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class DivineDamage(SpellEffect):
    DamageRange = (0, 10)
    StandardCast = "Holy light pierces {alias|target}!"

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of divine damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        self.target = self.get_target(lifeform, parameters)

        self.append_for_all_in_room(self.mutate(self.StandardCast))
        divine_damage = [Damage('divine', self.DamageRange, 'sense',( random.uniform, (0,1)))]
        damages = [(x.roll(lifeform), 'divine') for x in divine_damage]
        self.cmd.inflict_damage(self.target, damages)
