class Overwhelm:
    '''
    Overwhelm is an attack command which can knock an enemy off balance or even topple them.
    This comes at a cost, as an unsuccessful attack can cause the attacker to become off balance
    himself.
    '''
    Name = 'Overwhelm'

    def bonus(level):
        return 100 + 5*(level-1)

    def current_level_description(self):
        bonus_text = '' if self.level == 1 else '; gains {}% bonus against and for overwhelm rolls.'
        return 'Allows the player to use "Overwhelm", an offensive maneuver which can knock an enemy off balance or even topple them{}'.format(bonus_text)

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        return '; +5% bonus against and for overwhelm rolls'
