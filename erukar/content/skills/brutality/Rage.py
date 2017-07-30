from erukar.system.engine import Skill

class Rage(Skill):
    '''
    Rage grants the player to give himself the Enraged condition as a skill. The level of this
    skill improves the maximum resolve score that can be used in the condition, as well as the 
    duration.
    '''
    Name = 'Rage'

    def current_level_description(self):
        return 'Grants access to Rage; lasts {} rounds and adds up to {} Resolve'.format(\
            Rage.duration_at_level(self.level),\
            Rage.modifier_at_level(self.level))

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        return '+2 rounds duration, +4 maximum resolve modifier'

    def duration_at_level(level):
        return 2 * (level+1)

    def modifier_at_level(level):
        return 4 * level
