from erukar.system.engine import Condition


class Wither(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Wither'
    Participle  = 'Withering'
    Description = 'Decreases physical stats by 25%'

    def modify_strength(self, lf, amt):
        return -(lf.strength * 0.25)

    def modify_dexterity(self, lf, amt):
        return -(lf.dexterity * 0.25)

    def modify_vitality(self, lf, amt):
        return -(lf.vitality * 0.25)
