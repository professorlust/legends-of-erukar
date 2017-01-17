from .TextFormatter import TextFormatter

class DamageFormatter(TextFormatter):
    You = 'You {verb} {amount} damage!'
    They = '{target} {verb}s {amount} damage.'

    def get_damage_specifics(damage_result, specific='amount_deflected'):
        return ', '.join(['{} {}'.format(getattr(x, specific), x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])

    def process_and_append_damage_result(cmd, damage_result):
        attacker_results, target_results = DamageFormatter.get_string_results(damage_result)
        cmd.append_if_uid(cmd.target, '\n'.join(target_results))
        cmd.append_result(cmd.sender_uid, '\n'.join(attacker_results))

    def get_string_results(damage_result):
        attacker_results = []
        target_results = []

        DamageFormatter.append_deflection_results(damage_result, attacker_results, target_results)
        DamageFormatter.append_mitigation_results(damage_result, attacker_results, target_results)
        DamageFormatter.append_damage_results(damage_result, attacker_results, target_results)
        DamageFormatter.append_death_results(damage_result, attacker_results, target_results)

        return attacker_results, target_results

    def append_damage_results(damage_result, attacker_results, target_results):
        damage = DamageFormatter.get_damage_specifics(damage_result, 'amount_dealt')
        DamageFormatter.append_results_for_verb(damage, damage_result.victim, 'take', attacker_results, target_results)

        if damage_result.caused_incapacitated:
           target_results.append('You have been incapacitated by {}!'.format(damage_result.instigator.alias()))
           attacker_results.append('You have incapacitated {}!'.format(damage_result.victim.alias()))

    def append_deflection_results(damage_result, attacker_results, target_results):
        deflection = DamageFormatter.get_damage_specifics(damage_result, 'amount_deflected')
        DamageFormatter.append_results_for_verb(deflection, damage_result.victim, 'deflect', attacker_results, target_results)

    def append_mitigation_results(damage_result, attacker_results, target_results):
        mitigation = DamageFormatter.get_damage_specifics(damage_result, 'amount_mitigated')
        DamageFormatter.append_results_for_verb(mitigation, damage_result.victim, 'mitigate', attacker_results, target_results)

    def append_results_for_verb(results, victim, verb, attacker_results, target_results):
        if len(results) > 0:
            target_results.append(DamageFormatter.You.format(verb, results))
            attacker_results.append(DamageFormatter.They.format(victim.alias(), verb, results))

    def append_death_results(damage_result, attacker_results, target_results):
        target_results.append('You have been slain by {}...'.format(damage_result.instigator.alias()))
        attacker_results.append('You have slain {}!'.format(damage_result.victim.alias()))

