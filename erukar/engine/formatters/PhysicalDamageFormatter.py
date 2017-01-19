from .DamageFormatter import DamageFormatter

class PhysicalDamageFormatter(DamageFormatter):
    def process_and_append_damage_result(cmd, attack_roll, weapon, damage_result):
        attacker_results, target_results = DamageFormatter.get_string_results(damage_result)

        attacker_results.insert(0, 'Your attack ({}) with {} hits {}!'.format(attack_roll, weapon.alias(), damage_result.victim.alias()))
        target_results.insert(0, 'You are hit with {}\'s {} ({})!'.format(damage_result.instigator.alias(), weapon.alias(), attack_roll))

        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def append_missed_attack_results(cmd, weapon, attack_roll, victim, instigator):
        cmd.append_result(cmd.sender_uid, 'Your attack ({}) with {} misses {}.'.format(attack_roll, weapon.alias(), victim.alias()))
        cmd.append_if_uid(victim, 'You dodge {}\'s {} ({})!'.format(instigator.alias(), weapon.alias(), attack_roll))
