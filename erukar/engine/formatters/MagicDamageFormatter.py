from .TextFormatter import TextFormatter

class MagicDamageFormatter(TextFormatter):
    def process_and_append_damage_result(cmd, damage_result):
        attacker_results, target_results = MagicDamageFormatter.get_string_results(damage_result, cmd.target, cmd.caster)
        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def get_string_results(damage_result, target, caster):
        if damage_result.stopped_by_deflection:
            return MagicDamageFormatter.get_deflection_results(damage_result, target)

        if damage_result.stopped_by_mitigation:
            return MagicDamageFormatter.get_mitigation_results(damage_result, target, caster)

        if damage_result.caused_death:
            return MagicDamageFormatter.get_death_results(target, caster)
        
        return MagicDamageFormatter.get_damage_results(damage_result, target, caster)

    def get_deflection_results(damage_result, target):
        damage_string = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports])
        target_results = ['You deflect all {} damage!'.format(damage_string)]
        attacker_results = ['{} deflects all {} damage.'.format(target.alias(), damage_string)]
        return attacker_results, target_results

    def get_mitigation_results(damage_result, target):
        attacker_results = []
        target_results = []

        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])

        if len(deflection) > 0:
            target_results.append('You deflect {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflects {} damage.'.format(target.alias(), deflection))

        target_results.append('You mitigate {} damage, preventing you from taking any damage!'.format(mitigation))
        attacker_results.append('{} mitigates the remaining {} damage.'.format(target.alias(), mitigation))
        
        return attacker_results, target_results

    def get_damage_results(damage_result, target, caster):
        attacker_results = []
        target_results = []
        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])
        actual_damage = ', '.join(['{} {}'.format(x.amount_dealt, x.damage_type) for x in damage_result.reports if x.amount_dealt > 0])

        if len(deflection) > 0:
            target_results.append('You deflect {} damage!'.format(deflection))
            attacker_results.append('{} deflects {} damage.'.format(target.alias(), deflection))

        if len(mitigation) > 0:
            target_results.append('You mitigate {} damage!'.format(deflection))
            attacker_results.append('{} mitigates {} damage.'.format(target.alias(), deflection))

        target_results.append('You take {} damage!'.format(actual_damage))
        attacker_results.append('{} takes {} damage!'.format(target.alias(), actual_damage))

        if damage_result.caused_incapacitated:
           target_results.append('You have been incapacitated by {}!'.format(caster.alias()))
           attacker_results.append('You have incapacitated {}!'.format(target.alias()))

        return attacker_results, target_results

    def get_death_results(target, caster):
        target_results = ['You have been slain by {}...'.format(caster.alias())]
        attacker_results = ['You have slain {}!'.format(target.alias())]

        return attacker_results, target_results
