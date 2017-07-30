from erukar.system.engine import Skill

class ArcaneGift(Skill):
    '''
    The player is able to tap into sources of arcane energy. There is no cap on the levels for this
    skill, but the levels provide diminishing returns. Arcane Energy always regenerates at 5% of max
    per turn
    '''
    Name = 'Arcane Gift'
        
    def current_level_description(self):
        return 'Grants {} Arcane Energy to be used as an Arcane Source'.format(self.arcane_energy())

    def next_level_description(self):
        next_level = ArcaneGift.energy_at_level(self.level+1) - self.arcane_energy()
        return '+{} Arcane Energy'.format(next_level)

    def arcane_energy(self):
        '''
        Level  1 -  4: +25 Arcane Energy
        Level  5 -  9: +20 Arcane Energy
        Level 10 - 19: +10 Arcane Energy
        Level 20+    :  +5 Arcane Energy
        '''
        return ArcaneGift.energy_at_level(self.level)

    def energy_at_level(level):
        if level < 5:
            return 25 * level
        if level < 10:
            return 20 * (level+1)
        if level < 20:
            return 10 * (level+10)
        return 5 * (level+40)

    def apply_to(self, skilled):
        skilled.maximum_arcane_energy = self.maximum_arcane_energy

    def maximum_arcane_energy(self):
        return ArcaneGift.energy_at_level(self.level)

