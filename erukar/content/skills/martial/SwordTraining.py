from erukar.system.engine import Skill

class SwordTraining(Skill):
    Name = 'Sword Expertise'

    def current_level_description(self):
        return 'Improves weapon scaling with all Swords by +{}'.format(self.scalar_at(self.level))

    def next_level_description(self):
        return 'Further improves weapon scaling with all Swords by 0.25 (up to {})'.format(self.scalar_at(self.level+1))

    def scalar_at(self, level):
        return 0.25*level

    def apply_to(self, skilled):
        skilled.offset_scale_for_sword = self.offset_scale_for_sword

    def offset_scale_for_sword(self):
        return self.scalar_at(self.level)

