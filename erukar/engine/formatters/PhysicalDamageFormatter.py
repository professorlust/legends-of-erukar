from .DamageFormatter import DamageFormatter

class PhysicalDamageFormatter(DamageFormatter):
    def process_and_append_damage_result(cmd, attack_roll, weapon, damage_result):
        cmd.append_result(cmd.sender_uid, 'Your attack ({}) with {} hits {}!'.format(attack_roll, weapon, damage_result.victim.alias()))
        cmd.append_if_uid(damage_result.victim, 'You are hit with {}\'s {} ({})!'.format(damage_result.instigator.alias(), weapon, attack_roll))
        DamageFormatter.process_and_append_damage_result(cmd, damage_result)
