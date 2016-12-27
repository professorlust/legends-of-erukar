from erukar.engine.model.Describable import Describable
import erukar

class MagicBase(Describable):
    def on_cast(self, command, caster, parameters=None, efficacy=1.0):
        self.cmd = command
        self.caster = caster
        self.set_parameters(parameters)

    def set_parameters(self, parameters):
        '''Attempt to set parameters to the object. Sometimes this
        can fail, so it's wrapped in a try/catch to continue.'''
        if not parameters: return
        for param in parameters:
            try: setattr(self, param, parameters[param])
            except: pass

    def append_result(self, uid, msg):
        if self.cmd:
            self.cmd.append_result(uid, msg)

    def append_for_others_in_room(self, msg):
        if not self.cmd: return
        for content in self.caster.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not self.caster:
                self.cmd.append_result(content.uid, msg)

    def append_for_all_in_room(self, msg):
        if not self.cmd: return
        for content in self.caster.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform):
                self.cmd.append_result(content.uid, msg)

    def process_and_append_damage_result(self, damage_result):
        if damage_result.stopped_by_deflection:
            self.append_deflection_results(damage_result)
            return

        if damage_result.stopped_by_mitigation:
            self.append_mitigation_results(damage_result)
            return

        if damage_result.caused_death:
            self.append_death_results(damage_result)
            return
        
        self.append_damage_results(damage_result)

    def append_deflection_results(self, damage_result):
        damage_string = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports])
        self.cmd.append_if_uid(self.target, 'You deflect all {} damage!'.format(damage_string))
        self.cmd.append_result(self.cmd.sender_uid, '{} deflects all {} damage.'.format(self.target.alias(), damage_string))

    def append_mitigation_results(self, attack_roll, weapon, damage_result):
        attacker_results = []
        target_results = []

        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])

        if len(deflection) > 0:
            target_results.append('You deflect {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflects {} damage.'.format(self.target.alias(), deflection))

        target_results.append('You mitigate {} damage, preventing you from taking any damage!'.format(mitigation))
        attacker_results.append('{} mitigates the remaining {} damage.'.format(self.target.alias(), mitigation))
        
        self.cmd.append_if_uid(self.target, '\n'.join(target_results))
        self.cmd.append_result(self.cmd.sender_uid, '\n'.join(attacker_results))

    def append_damage_results(self, damage_result):
        attacker_results = []
        target_results = []
        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])
        actual_damage = ', '.join(['{} {}'.format(x.amount_dealt, x.damage_type) for x in damage_result.reports if x.amount_dealt > 0])

        if len(deflection) > 0:
            target_results.append('You deflect {} damage!'.format(deflection))
            attacker_results.append('{} deflects {} damage.'.format(self.target.alias(), deflection))

        if len(mitigation) > 0:
            target_results.append('You mitigate {} damage!'.format(deflection))
            attacker_results.append('{} mitigates {} damage.'.format(self.target.alias(), deflection))

        target_results.append('You take {} damage!'.format(actual_damage))
        attacker_results.append('{} takes {} damage!'.format(self.target.alias(), actual_damage))

        if damage_result.caused_incapacitated:
           target_results.append('You have been incapacitated by {}\'s {}!'.format(self.caster.alias(), weapon.alias()))
           attacker_results.append('You have incapacitated {}!'.format(self.target.alias()))

        self.cmd.append_if_uid(self.target, '\n'.join(target_results))
        self.cmd.append_result(self.cmd.sender_uid, '\n'.join(attacker_results))

    def append_death_results(self, weapon, damage_result):
        attacker_results = []
        target_results = []
        target_results.append('You have been slain by {}...'.format(self.caster.alias()))
        attacker_results.append('You have slain {}!'.format(self.target.alias()))

        self.cmd.append_if_uid(self.target, '\n'.join(target_results))
        self.cmd.append_result(self.cmd.sender_uid, '\n'.join(attacker_results))
