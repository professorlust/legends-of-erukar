from erukar.system.engine import Skill


class WandTraining(Skill):
    Name = 'Wand Expertise'
    Current = 'Improves weapon scaling with all Wands by +{}'
    Next = 'Further improves weapon scaling with all Wands by 0.25 (up to {})'

    def current_level_description(self):
        return self.Current.format(self.scalar_at(self.level))

    def next_level_description(self):
        return self.Next.format(self.scalar_at(self.level+1))

    def scalar_at(self, level):
        return 0.25*level

    def apply_to(self, skilled):
        skilled.offset_scale_for_wand = self.offset_scale_for_wand

    def offset_scale_for_wand(self):
        return self.scalar_at(self.level)

    def meets_requirements(player):
        return player.acuity >= 5
