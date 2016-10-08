from erukar.engine.model.SpellEffect import SpellEffect
import random

class HealEffect(SpellEffect):
    AlreadyFull = "The healing had no effect, as {lifeform}'s health was already full."
    StandardCast = "Brilliant light radiates from {lifeform}'s wounds. {lifeform} regains {health} health and the wounds slowly close."

    def on_cast(self, lifeform, efficacy=1.0):
        if lifeform.health == lifeform.max_health:
            return self.AlreadyFull.format(lifeform=lifeform.alias())

        health = int(random.uniform(3, 8))
        lifeform.health = min(lifeform.max_health, lifeform.health + health)
        return self.StandardCast.format(lifeform=lifeform.alias(), health=health)
