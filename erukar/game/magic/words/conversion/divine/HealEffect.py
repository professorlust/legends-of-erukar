from erukar.engine.magic.SpellWord import SpellWord
import random

class HealEffect(SpellWord):
    AlreadyFull = "The healing had no effect, as {target}'s health was already full."
    StandardCast = "Brilliant light radiates from {target}'s wounds. {target} regains {health} health and the wounds slowly close."

    PotionName = 'Healing'
    PotionPriceMultiplier = 9.0

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Heals a specific target, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters, efficacy)

        if self.target.health == self.target.max_health:
            self.append_result(lifeform.uid, self.AlreadyFull.format(target=self.target.alias()))
            self.append_for_others_in_room(self.AlreadyFull.format(target=self.target.alias()))
            return

        health = int(random.uniform(3, 8))
        self.target.health = min(self.target.max_health, self.target.health + health)
        self.cmd.dirty(self.target)
        self.append_result(lifeform.uid, self.StandardCast.format(target=self.target.alias(), health=health))
        self.append_for_others_in_room(self.StandardCast.format(target=self.target.alias(), health=health))
