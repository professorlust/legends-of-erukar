from erukar.engine.model.SpellEffect import SpellEffect
from erukar.game.conditions.magical.AugmentedWeapon import AugmentedWeapon
import erukar, random

class InflictCondition(SpellEffect):
    CasterResult = "You feel the energy inside of you concentrate, then you release the energy in a faint blast of golden light which ripples through the air!"
    ViewerResult = "A blast of thin golden light ripples outward from {alias|caster}, colliding with {alias|target}!."
    TargetResult = "Your vision blurs as the force nearly knocks you to your feet. You feel disoriented!"

    ConditionType = 'Disoriented'

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of fire damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        
        condition = getattr(erukar.game.conditions, self.ConditionType)(self.target)
        condition.Duration = int(condition.Duration * efficacy)

        self.append_result(self.caster.uid, self.mutate(self.CasterResult))
        self.append_for_others_in_room(self.mutate(self.ViewerResult))
        self.append_result(self.target.uid, self.mutate(self.TargetResult))

        self.target.conditions.append(condition)

        return parameters

