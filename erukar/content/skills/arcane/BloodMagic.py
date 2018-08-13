from erukar.system.engine import Skill


class BloodMagic(Skill):
    Name = 'Arcane Gift'
    MinHealth = 1
    Current = 'Allows for consumption of own lifeforce in order '\
        'to create arcane energy. Consumes {} health to create '\
        '{} arcane energy.'
    NextWithHealth = 'Increases energy gained per health point '\
        'lost to {:0.0f} and decreases health lost to {}. This '\
        'effectively increases overall energy gained by {}, to '\
        '{} in total.'
    Next = 'Increases energy gained per health point lost to '\
        '{}, effectively increasing overall energy gained by {} '\
        'to a total of {} energy.'

    def current_level_description(self):
        return self.Current.format(
            int(self.health_consumed()),
            int(self.energy_created())
        )

    def health_consumed(self):
        return BloodMagic._health(self.level)

    def energy_created(self):
        return BloodMagic._energy(self.level)

    def _health(level):
        return 50

    def _energy(level):
        if level <= 5:
            return 0.5 + 0.1*level
        if level <= 15:
            return 0.75 + 0.05*level
        return 1.35 + 0.01*level

    def next_level_description(self):
        n_health = BloodMagic._health(self.level + 1)
        n_energy = BloodMagic._energy(self.level + 1)
        n_pool = n_health * n_energy
        d_health = self.health_consumed() - n_health
        d_pool = n_pool - self.health_consumed()*self.energy_created()
        if d_health > 0:
            return self.NextWithHealth.format(
                n_energy,
                n_health,
                d_pool,
                n_pool
            )
        return self.Next.format(
            n_energy,
            d_pool,
            n_pool
        )

    def create_energy(self, target):
        health = self.health_consumed()
        if health >= target.health:
            health = target.health - 1
        energy = int(health * self.energy_created())
        target.take_damage(int(health), target)
        return energy
