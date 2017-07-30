import copy

class ServerProperties:
    def __init__(self):
        '''The following are defaults and all can be overwritten via config/server/ scripts.'''
        # In ServerProperties.py
        self.PermaDeath = True
        self.StartingWealth = 1000
        self.StartingStatPoints = 15
        self.StartingSkillPoints = 2
        self.BaseHealth = 4
        self.BaseEvasion = 10

        # In Arcana.py
        self.SpellWords = {
            'thel': 'AugmentWeapon',
            'loth': 'ConditionBlinded',
            'loz':  'ConditionFrozen',
            'roth': 'DamageOverTime',
            'reth': 'DamageSingleTarget',
            'aoh':  'ElementalAcid',
            'rei':  'ElementalDemonic',
            'feth': 'ElementalDivine',
            'rik':  'ElementalElectricity',
            'zel':  'ElementalFire',
            'zohl': 'ElementalIce',
            'mohr': 'ElementalForce',
            'mar':  'HealEffect',
            'muun': 'InflictCondition',
            'nohs': 'Sunder',
        }

    def copy(self):
        return copy.deepcopy(self)
