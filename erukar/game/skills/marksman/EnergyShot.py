import math

class Energyshot:
    '''Energyshot infuses energy from a source into a projectile.'''
    Name = 'Energyshot'

    def energy_consumed(level):
        return level

    def damage_per_energy(level):
        return 4.0 + 0.5*(level-1)

    def current_level_description(self):
        return 'Allows the player to use "Energyshot", a magically-enhanced projectile; Energyshot consumes up to {} energy, providing {} extra damage per energy consumed'.format(Energyshot.energy_consumed(self.level_, Energyshot.extra_damage(self.level)))

    def next_level_description(self):
        if self.level >= 8:
            return 'None'
        return '+1 energy consumed per shot, +0.5 damage per energy consumed'
