from .DamageFormatter import DamageFormatter

class PhysicalDamageFormatter(DamageFormatter):
    def process_and_append_damage_result(cmd, attack_state):
        attacker_results, target_results = DamageFormatter.get_string_results(attack_state.processed_damage_result)

        attacker_results.insert(0, 'Your attack ({}) with {} hits {}!'.format(
            attack_state.attack_roll, 
            attack_state.weapon.alias(), 
            attack_state.target.alias()))
        target_results.insert(0, 'You are hit with {}\'s {} ({})!'.format(
            attack_state.attacker.alias(), 
            attack_state.weapon.alias(), 
            attack_state.attack_roll))

        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def append_missed_attack_results(cmd, attack_state):
        cmd.append_result(cmd.sender_uid, 'Your attack ({}) with {} misses {}.'.format(
            attack_state.attack_roll, 
            attack_state.weapon.alias(), 
            attack_state.target.alias()))
        cmd.append_if_uid(attack_state.target, 'You dodge {}\'s {} ({})!'.format(
            attack_state.attacker.alias(), 
            attack_state.weapon.alias(), 
            attack_state.attack_roll))
