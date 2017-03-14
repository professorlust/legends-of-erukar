from erukar.engine.model.Skill import Skill

class ArcaneGift(Skill):
    '''
    The player is able to tap into sources of arcane energy. There is no cap on the levels for this
    skill, but the levels provide diminishing returns. Arcane Energy always regenerates at 5% of max
    per turn

    '''
    def arcane_energy(self):
        '''
        Level  1 -  4: +25 Arcane Energy
        Level  5 -  9: +20 Arcane Energy
        Level 10 - 19: +10 Arcane Energy
        Level 20+    :  +5 Arcane Energy
        '''
        if self.level < 5:
            return 25 * self.level
        if self.level < 10:
            return 20 * (self.level+1)
        if self.level < 20:
            return 10 * (self.level+10)
        return 5 * (self.level+40)
