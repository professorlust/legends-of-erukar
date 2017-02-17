from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Observation import Observation
from erukar.engine.calculators.Modules import Modules
import random

class ChanceToInflictCondition(WeaponMod):
    Probability = 1
    Desirability = 8.0
    ShouldRandomizeOnApply = True

    Glances = [
    ]

    Inspects = [
    ]

    Levels = [
        'Unlikely',
        '',
        'Likely',
        'Probable',
        'Definite',
        'Absolute'
    ]

    PersistentAttributes = ['chance', 'minimum_rounds', 'maximum_rounds', 'condition_name', 'InventoryDescription', 'InventoryName']
    BaseInventoryDescription = "Has a {:3.1f}% chance to inflict {} on an enemy for {} to {} rounds on hit"

    def randomize(self, parameters=None):
        '''In the future we will determine level based on the generation parameters level and desirability''' 
        self.condition_name, self.condition = random.choice(list(Modules.get_members_of('erukar.game.conditions.negative')))

        self.level = int(random.random() * len(self.Levels))
        self.chance = 0.025 * (1 + self.level)
        self.minimum_rounds = 1 * (1 + self.level)
        self.maximum_rounds = 2 * (1 + self.level)
        self.InventoryName = ' '.join([self.Levels[self.level], self.condition.Noun]).strip()
        self.InventoryDescription = self.BaseInventoryDescription.format(100*self.chance, self.condition.Noun, self.minimum_rounds, self.maximum_rounds)

    def on_process_damage(self, attack_state, command):
        if not self.condition:
            self.condition = getattr(erukar, self.condition_name)

        if random.random() <= self.chance:
            effect = self.condition(attack_state.target, attack_state.attacker)
            attack_state.target.conditions.append(effect) 
       
#           command.append_result(attack_state.target.uid, effect.target_inflict_result)
#           command.append_result(attack_state.attacker.uid, effect.attacker_inflict_result.format(attack_state.target.alias()))

