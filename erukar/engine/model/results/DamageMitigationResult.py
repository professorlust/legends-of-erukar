class DamageMitigationResult:
    def __init__(self, damage=None):
        self.attacker_uid = ''
        self.receiver_uid = ''
        self.damage_type = '' if not damage else damage.name
        # damage values
        self.raw = 0
        self.amount_deflected = 0
        self.amount_mitigated = 0
        self.amount_dealt = 0
        # flags
        self.stopped_by_deflection = False
        self.stopped_by_mitigation = False

    def set_attacker(self, instigator):
        '''Try to get the uid from the instigator, if it exists'''
        if instigator and hasattr(instigator, 'uid'):
            self.instigator_uid = instigator.uid
