from erukar.system.engine import Skill, Lifeform

class DualWielding(Skill):
    Name = 'Dual Wielding'

    def current_penalty_reduction(self):
        return DualWielding.penalty_reduction(self.level)

    def penalty_reduction(level):
        return 5 * level

    def level_description(level):
        reduction = DualWielding.penalty_reduction(level)
        return 'Reduces dual wielding attack roll and damage penalties to {}% ({}% reduction)'.format(
            Lifeform.BaseDualWieldingPenalty - reduction,
            reduction
        )

    def current_level_description(self):
        return DualWielding.level_description(self.level)

    def next_level_description(self):
        if self.level < 8:
            return DualWielding.level_description(self.level+1)
        return ''
