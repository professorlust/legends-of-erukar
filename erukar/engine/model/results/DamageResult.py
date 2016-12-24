class DamageResult:
    def __init__(self, damage):
        self.string_results = {} # uid: results
        self.uids_to_corpsify = set() # Collection of UIDs to corpsify
        self.xp_awards = {} # uid: amount
        self.dealt_damage = False
        self.damage_amount = 0
        self.damage_type = damage.name

    def add_xp(self, instigator, amount):
        if not hasattr(instigator, 'uid'):
            return
        if instigator.uid not in self.xp_awards:
            self.xp_awards[instigator.uid] = 0
        self.xp_awards[instigator.uid] += amount

    def add_string_result(self, uid, result):
        if uid not in self.string_results:
            self.string_results[uid] = []
        self.string_results[uid].append(result)

    def corpsify(self, victim, killer=None):
        '''Mark something to become a corpse'''
        # Tell the victim they've been slain
        self.uids_to_corpsify.add(victim.uid)
        if killer:
            self.add_string_result(uid, 'You have been slain by {}!'.format(killer.alias()))
            self.add_string_result(killer.uid, 'You have slain {}'.format(victim.alias()))
            return
        self.add_string_result(victim.uid, 'You have been slain!')

    def is_corpsified(self, target):
        '''Check to see if a target is marked for corpsification'''
        return hasattr(target, 'uid') and target.uid in self.uids_to_corpsify

    def successful_deflection(self, deflector, instigator, raw):
        '''Handles appending results on a successful deflection'''
        if instigator:
            if hasattr(instigator, 'alias'):
                self.add_string_result(deflector.uid,'You successfully deflected all {} {} damage from {}!'.format(raw, self.damage_type, instigator.alias()))
            if hasattr(instigator, 'uid'):
                self.add_string_result(instigator.uid, '{} deflected all {} points of {} damage!'.format(deflector.alias(), raw, self.damage_type))
            return

        self.add_string_result(deflector.uid,'You successfully deflected all {} {} damage!'.format(raw, self.damage_type))

    def successful_mitigation(self, deflector, instigator, after_deflection, damage):
        '''handles all results on a successful mitigation'''
        if instigator:
            if hasattr(instigator, 'alias'):
                self.add_string_result(deflector.uid,'You successfully mitigated all {} {} damage from {}!'.format(after_deflection, self.damage_type, instigator.alias()))
            if hasattr(instigator, 'uid'):
                self.add_string_result(instigator.uid, '{} mitigated all {} points of {} damage!'.format(deflector.alias(), after_deflection, self.damage_type))
            return

        self.add_string_result(deflector.uid,'You successfully mitigated all {} {} damage!'.format(after_deflection, self.damage_type))

    def attack_successful(self, target, instigator, damage, amounts):
        self.dealt_damage = True
        self.damage_amount = amounts['total']
        if amounts['deflected'] > 0 or amounts['mitigated'] > 0:
            self.add_string_result(target.uid, 'You deflected {} and mitigated {} points of {} damage.'.format(amounts['deflected'], amounts['mitigated'], self.damage_type))
            self.add_string_result(instigator.uid, '{} deflected {} and mitigated {} points of {} damage.'.format(target.alias(), amounts['deflected'], amounts['mitigated'], self.damage_type))
