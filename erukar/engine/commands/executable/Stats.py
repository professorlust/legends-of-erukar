from erukar.engine.commands.Command import Command
from erukar.engine.model.Damage import Damage
from erukar.engine.lifeforms import Lifeform

class Stats(Command):
    NeedsArgs = False

    attribute_types = [
        "strength",
        "dexterity",
        "vitality",
        "acuity",
        "sense",
        "resolve"]

    def perform(self):
        pawn = self.args['player_lifeform']
        output_result = {
			'level': pawn.level,
			'xp': {
                'current': pawn.experience, 
                'nextLevel': pawn.calculate_necessary_xp()
            },
			'health': {'current': pawn.health, 'max': pawn.max_health},
			'evasion': pawn.evasion(),
			'equipLoad': {'current': pawn.equip_load(), 'max': pawn.max_equip_load()},
			'arcaneEnergy': {'current': pawn.arcane_energy, 'max': pawn.maximum_arcane_energy()},
			'strength':  {'base': pawn.strength, 'mod': Stats.get_mod(pawn, 'strength')},
			'dexterity': {'base': pawn.dexterity, 'mod': Stats.get_mod(pawn, 'dexterity')},
			'vitality':  {'base': pawn.vitality, 'mod': Stats.get_mod(pawn, 'vitality')},
			'acuity':    {'base': pawn.acuity, 'mod': Stats.get_mod(pawn, 'acuity')},
			'sense':     {'base': pawn.sense, 'mod': Stats.get_mod(pawn, 'sense')},
            'resolve':   {'base': pawn.resolve, 'mod': Stats.get_mod(pawn, 'resolve')},
            'mitigations': [],
            'conditions': []
        }

        for damage in Damage.Types:
            output_result['mitigations'].append({
                'type': damage.capitalize(),
                'deflection': pawn.deflection(damage),
                'mitigation': int(100.0 * (1 - pawn.mitigation(damage)))
            })

        for condition in pawn.conditions:
            output_result['conditions'].append({
                'name': condition.name(),
                'description': condition.describe(),
                'durationRemaining': condition.duration_remaining(),
                'isNegative': False
            })

        self.append_result(self.player_info.uuid, output_result)
        return self.succeed()

    def get_mod(pawn, stat):
        return pawn.calculate_effective_stat(stat) - getattr(pawn, stat)
