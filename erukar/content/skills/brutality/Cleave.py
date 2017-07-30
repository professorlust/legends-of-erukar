class Cleave:
    '''
    Cleave splits damage with weapons between up to N targets in the same room as the player.
    Weapon must be melee and an enemy cannot be chosen twice. 
    '''
    Name = 'Cleave'

    def max_targets(level):
        return 1 + math.ceil((level+1)/4)

    def damage_reduction(level):
        return 80 - 5 * level

    def current_level_description(self):
        return 'Allows "Cleave", which allows an attacker to split damage from slashing or bludgeoning weapon between {} targets, reducing damage per target by {}%.'.format(Cleave.max_targets(self.level), Cleave.damage_reduction(self.level))

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        if self.max_targets(self.level+1) > self.max_targets(self.level):
            return '+1 additional target; Total Damage Reduction reduced by 5%'
        return 'Total Damage Reduction reduced by 5%'
