from erukar.game.modifiers.inventory.base.ChanceOnHitModifier import ChanceOnHitModifier
from erukar.game.conditions.negative.Frozen import Frozen
from erukar.engine.model.Observation import Observation

class Freezing(ChanceOnHitModifier):
    Probability = 1
    Desirability = 8.0

    Glances = [
    ]

    Inspects = [
    ]

    InventoryName = "Freezing"
    InventoryDescription = "Has a 5% chance to freeze target on hit"

    def do_chance_effect(self, attack_state, command):
       frozen = Frozen(attack_state.target, attack_state.attacker)
       attack_state.target.conditions.append(frozen) 
       
       command.append_result(attack_state.target.uid, 'You rapidly freeze over!')
       command.append_result(attack_state.attacker.uid, '{} rapidly freezes over!'.format(attack_state.target.alias()))
