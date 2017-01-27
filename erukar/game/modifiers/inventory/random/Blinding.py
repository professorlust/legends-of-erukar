from erukar.game.modifiers.inventory.base.ChanceOnHitModifier import ChanceOnHitModifier
from erukar.game.conditions.negative.Frozen import Frozen
from erukar.engine.model.Observation import Observation

class Blinding(ChanceOnHitModifier):
    Probability = 1
    Desirability = 8.0

    Glances = [
    ]

    Inspects = [
    ]

    InventoryName = "Blinding"
    InventoryDescription = "Has a 5% chance to blind an enemy for [1, 2] rounds on hit"

    def do_chance_effect(self, attack_state, command):
       frozen = Frozen(attack_state.target, attack_state.attacker)
       attack_state.target.conditions.append(frozen) 
       
       command.append_result(attack_state.target.uid, 'A burst of light flashes in front of your eyes and the whole room goes dark!')
       command.append_result(attack_state.attacker.uid, '{} experiences a bright flash in front of his eyes, blinding him!'.format(attack_state.target.alias()))
