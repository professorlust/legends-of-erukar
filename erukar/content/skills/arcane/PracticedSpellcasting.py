from erukar.system.engine import Skill


class PracticedSpellcasting(Skill):
    Name = 'Practiced Spellcasting'
    Current = 'Can cast spells with {} Energy at 100% efficiency'
    Next = '+{} Max Energy for 100%'

    def max_effective_arcane_energy(self):
        return PracticedSpellcasting.max_arc_at_level(self.level)

    def current_level_description(self):
        return self.Current.format(self.max_effective_arcane_energy())

    def next_level_description(self):
        diff = PracticedSpellcasting.d_efficiency(self.level)
        return self.Next.format(diff)

    def d_efficiency(level_i, level_f=-1):
        level_f = level_f if level_f > 0 else level_i + 1
        initial = PracticedSpellcasting.max_arc_at_level(level_i)
        final = PracticedSpellcasting.max_arc_at_level(level_f)
        return final - initial

    def max_arc_at_level(level):
        return 5 * level
