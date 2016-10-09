from erukar.engine.model.SpellEffect import SpellEffect
import random

class HealEffect(SpellEffect):
    AlreadyFull = "The healing had no effect, as {lifeform}'s health was already full."
    StandardCast = "Brilliant light radiates from {lifeform}'s wounds. {lifeform} regains {health} health and the wounds slowly close."

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Heals a specific target, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters, efficacy)
        target = self.get_target(lifeform, parameters)
        if target.health == target.max_health:
            self.append_result(lifeform.uid, self.AlreadyFull.format(target=target.alias()))
            self.append_for_others_in_room(target.uid, self.AlreadyFull.format(target=target.alias()))
            return

        health = int(random.uniform(3, 8))
        target.health = min(target.max_health, target.health + health)
        self.append_result(lifeform.uid, self.StandardCast.format(lifeform=target.alias(), health=health))
        self.append_for_others_in_room(self.StandardCast.format(lifeform=target.alias(), health=health))
