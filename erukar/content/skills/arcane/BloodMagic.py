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
        if level <= 10:
            return 10 - level/2
        return 5.0

    def _energy(level):
        if level < 10:
            return (level+1) * 2
        return 19.75 + level/4

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

    def apply_to(self, skilled):
        if self not in skilled.secondary_energy_sources:
            skilled.secondary_energy_sources.append(self)

    def create_energy(self, target):
        health = self.health_consumed()
        if health >= target.health:
            health = target.health - 1
        energy = int(health * self.energy_created())
        target.take_damage(int(health), target)
        return energy
