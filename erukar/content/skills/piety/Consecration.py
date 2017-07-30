from erukar.system.engine import Skill

class Consecration(Skill):
    '''
    Consecration allows the player to actively sanctify areas of the world through the use of special
    Divine Words. At Level 5, the player gains access to an aura which can auto-bless areas at a 
    lower rate than the active.
    '''
    Name = 'Consecration'

    def aura_available(level):
        return level > 4

    def efficiency_bonus(level):
        return 5 * (level-1)

    def current_level_description(self):
        return ''.join([
            #'Allows usage of "Consecration", a spell which purges demonic energy and creates divine energy.',
            Consecration.eff_bonus_description(self.level),
            Consecration.aura_description(self.level),
        ])

    def aura_description(level):
        if Consecration.aura_available(level):
            return 'Allows usage of Consecration with the Aura spell word. '
        return ''
    
    def eff_bonus_description(level):
        bonus = Consecration.efficiency_bonus(level)
        if bonus > 0:
            return 'Provides a {}% efficiency bonus to Consecration. '.format(bonus)
        return ''
