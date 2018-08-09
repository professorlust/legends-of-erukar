from erukar.system.engine import Skill


class ArcaneEnergy(Skill):
    Name = 'Arcane Gift'
    Current = 'Grants {} Arcane Energy to be used as an Arcane Source'

    def current_level_description(self):
        return self.Current.format(self.arcane_energy())

    def next_level_description(self):
        next_level = ArcaneEnergy.energy_at_level(self.level+1)
        diff = next_level - self.arcane_energy()
        return '+{} Arcane Energy'.format(diff)

    def arcane_energy(self):
        return ArcaneEnergy.energy_at_level(self.level)

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
        return ArcaneEnergy.energy_at_level(self.level)
