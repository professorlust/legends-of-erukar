from erukar.system.engine import Condition


class Dodging(Condition):
    IsTemporary = True
    RemoveOnStartOfTurn = True
    Duration = 0
    Incapacitates = False
    EvasionBonus = 0.25

    Noun = 'Dodge Prepared'
    Participle = 'Preparing Dodge'
    Description = 'You have prepared a dodge, granting {}% bonus evasion'

    def modify_evasion(self, caller, evasion):
        if caller is self.target:
            return (1 + self.EvasionBonus) * evasion
        return evasion
