from erukar.system.engine import Skill

class Bloodlust(Skill):
    '''
    Adds the Bloodlust condition to the player when an enemy is below a specific health threshold.
    Additional levels increase the duration and bonuses provided.
    '''
    Name = 'Bloodlust'

    def duration(level):
        return 2 * (level + 1)

    def bonus_resolve(level):
        return 2 * level

    def trigger_percentage(level):
        return 20 + level * 5

    def current_level_description(self):
        return 'Grants +{} resolve while a nearby enemy is below {}% health; lasts {} rounds after enemy dies'.format(Bloodlust.bonus_resolve(self.level), Bloodlust.trigger_percentage(self.level), Bloodlust.duration(self.level))

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        return '+2 resolve added, +5% health threshold, +2 round duration'
