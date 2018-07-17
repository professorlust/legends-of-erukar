from erukar.system.engine import Damage
from ..Command import Command


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
            'health': {
                'current': pawn.health,
                'max': pawn.maximum_health()
            },
            'evasion': pawn.evasion(),
            'equipLoad': {
                'current': pawn.equip_load(),
                'max': pawn.max_equip_load()
            },
            'arcaneEnergy': {
                'current': pawn.arcane_energy,
                'max': pawn.maximum_arcane_energy()
            },
            'mitigations': [],
            'conditions': []
        }

        for attribute in Stats.attribute_types:
            output_result[attribute] = Stats.format_stat(pawn, attribute)

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

        self.append_result(self.player_info.uid, output_result)
        return self.succeed()

    def get_mod(pawn, stat):
        return pawn.calculate_effective_stat(stat) - getattr(pawn, stat)

    def format_stat(player, stat):
        return {
            'base': getattr(player, stat),
            'mod': Stats.get_mod(player, stat)
        }
