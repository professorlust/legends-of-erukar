from erukar.system.engine import Skill

class Charge(Skill):
    '''
    Charge executes both a move command and an attack command on the same turn, but reduces
    efficacy of the attack and reduces the player's evasion until the next turn.
    '''
    Name = 'Charge'

    def evasion_penalty(level):
        return 2 * level

    def attack_efficacy(level):
        return 40 + 5 * level

    def current_level_description(self):
        return 'Allows the player to use "Charge", a combined move and attack; the attack roll incurs a {}% penalty and the player\'s evasion is temporarily reduced by {}'.format(100-Charge.attack_efficacy(self.level), Charge.evasion_penalty(self.level))

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        return 'Evasion penalty reduced by 2, attack efficiency increased by 5%'
