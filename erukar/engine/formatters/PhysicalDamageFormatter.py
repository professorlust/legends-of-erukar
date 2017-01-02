from .TextFormatter import TextFormatter

class PhysicalDamageFormatter(TextFormatter):
    def append_missed_attack_results(cmd, attack_roll):
        attacker_results, target_results = PhysicalDamageFormatter.get_missed_attack_results(attack_roll, cmd.character, cmd.target)
        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def process_and_append_damage_result(cmd, attack_roll, weapon, damage_result):
        attacker_results, target_results = PhysicalDamageFormatter.get_string_results(attack_roll, cmd.character, cmd.target, weapon, damage_result)
        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def get_string_results(attack_roll, attacker, target, weapon, damage_result):
        if damage_result.stopped_by_deflection:
            return PhysicalDamageFormatter.get_deflection_results(attack_roll, attacker, target)

        if damage_result.stopped_by_mitigation:
            return PhysicalDamageFormatter.get_mitigation_results(attack_roll, attacker, target, weapon, damage_result)

        if damage_result.caused_death:
            return PhysicalDamageFormatter.get_death_results(attacker, target)
        
        return PhysicalDamageFormatter.get_damage_results(attack_roll, attacker, target, weapon, damage_result)

    def get_missed_attack_results(attack_roll, attacker, target):
        target_results = ['{} missed an attack against you!'.format(attacker.alias())]
        attacker_results = ['Your attack ({}) missed {}!'.format(attack_roll, target.alias())]
        return attacker_results, target_results

    def get_deflection_results(attack_roll, attacker, target, weapon, damage_result):
        damage_string = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports])
        target_results = ['{}\'s attack with {} hits you, but you deflect all {} damage!'.format(attacker.alias(), weapon.alias(), damage_string)]
        attacker_results = ['Your attack ({}) with {} hits {}, but all {} damage is deflected!'.format(attack_roll, weapon.alias(), target.alias(), damage_string)]

        return attacker_results, target_results

    def get_mitigation_results(attack_roll, attacker, target, weapon, damage_result):
        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])

        target_results = ['{}\'s attack with {} hits you!'.format(attacker.alias(), weapon.alias())]
        attacker_results = ['Your attack ({}) with {} hits {}!'.format(attack_roll, weapon.alias(), target.alias())]

        if len(deflection) > 0:
            target_results.append('Your armor deflects {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflects {} damage.'.format(target.alias(), deflection))

        target_results.append('Your armor mitigates {} damage, preventing you from taking any damage!'.format(mitigation))
        attacker_results.append('{}\'s armor mitigates the remaining {} damage.'.format(target.alias(), mitigation))

        return attacker_results, target_results

    def get_damage_results(attack_roll, attacker, target, weapon, damage_result):
        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])
        actual_damage = ', '.join(['{} {}'.format(x.amount_dealt, x.damage_type) for x in damage_result.reports if x.amount_dealt > 0])

        target_results = ['{}\'s attack with {} hits you!'.format(attacker.alias(), weapon.alias())]
        attacker_results = ['Your attack ({}) with {} hits {}!'.format(attack_roll, weapon.alias(), target.alias())]

        if len(deflection) > 0:
            target_results.append('Your armor deflects {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflects {} damage.'.format(target.alias(), deflection))

        if len(mitigation) > 0:
            target_results.append('Your armor mitigates {} damage!!'.format(mitigation))
            attacker_results.append('{}\'s armor mitigates {} damage.'.format(target.alias(), mitigation))

        target_results.append('You take {} damage!'.format(actual_damage))
        attacker_results.append('{} takes {} damage!'.format(target.alias(), actual_damage))

        if damage_result.caused_incapacitated:
            target_results.append('You have been incapacitated by {}\'s {}!'.format(attacker.alias(), weapon.alias()))
            attacker_results.append('You have incapacitated {}!'.format(target.alias()))
       
        return attacker_results, target_results

    def get_death_results(attacker, target):
        target_results = ['You have been slain by {}...'.format(attacker.alias())]
        attacker_results = ['You have slain {}!'.format(target.alias())]

        return attacker_results, target_results

