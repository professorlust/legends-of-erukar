from erukar.engine.model.Skill import Skill

class Desecration(Skill):
    '''
    Desecration allows the player to actively sanctify areas of the world through the use of special
    Divine Words. At Level 5, the player gains access to an aura which can auto-bless areas at a 
    lower rate than the active.
    '''
    Name = 'Desecration'

    def aura_available(level):
        return level > 4

    def efficiency_bonus(level):
        return 5 * (level-1)

    def current_level_description(self):
        return ''.join([
            #'Allows usage of "Desecration", a spell which purges demonic energy and creates divine energy.',
            Desecration.eff_bonus_description(self.level),
            Desecration.aura_description(self.level),
        ])

    def aura_description(level):
        if Desecration.aura_available(level):
            return 'Allows usage of Desecration with the Aura spell word. '
        return ''
    
    def eff_bonus_description(level):
        bonus = Desecration.efficiency_bonus(level)
        if bonus > 0:
            return 'Provides a {}% efficiency bonus to Desecration. '.format(bonus)
        return ''
