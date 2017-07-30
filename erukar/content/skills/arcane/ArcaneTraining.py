from erukar.system.engine import Skill

class ArcaneTraining(Skill):
    Name = 'Arcane Training'

    Descriptions = [
        'Initiate',
        'Novice',
        'Advanced Beginner',
        'Competent',
        'Proficient',
        'Adept',
        'Expert',
        'Master',
    ]

    def max_effective_arcane_energy(self):
        return ArcaneTraining.max_arc_at_level(self.level)

    def current_level_description(self):
        return '{}: Can cast spells with {} Energy at 100% efficiency'.format(\
                self.Descriptions[self.level-1],\
                self.max_effective_arcane_energy())

    def next_level_description(self):
        if self.level >= len(self.Descriptions):
            return 'None'
        diff = ArcaneTraining.max_arc_at_level(self.level + 1) - ArcaneTraining.max_arc_at_level(self.level)
        return '{} (+{} Max Energy for 100%)'.format(self.Descriptions[self.level], diff)

    def max_arc_at_level(level):
        return 5 * level
