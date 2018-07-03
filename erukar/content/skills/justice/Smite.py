from erukar.system.engine import Attack, Damage, DamageScalar


class Smite(Attack):
    Name = 'Smite'
    ShowInLists = True
    Description = 'Smite {} with {}'
    CurrentLevel = 'Channel Divine or Demonic energy through '\
        'a melee weapon, inflicting an additional {:0.0f}% of total '\
        'damage. Costs two action points.'
    NextLevel = 'Increases percentage of damage to {:0.0f}%.'

    def ap_cost(self, *_):
        return 2

    def modify_damage(self, damage):
        damage += [(self.damage(damage), 'divine')]
        return damage

    def damage(self, damages):
        raw_total = sum(x[0] for x in damages)
        return int(raw_total * Smite.multiplier(self.level))

    def multiplier(level):
        return 0.5 + 0.25*level

    def current_level_description(self):
        percent = Smite.multiplier(self.level) * 100.0
        return self.CurrentLevel.format(percent)

    def next_level_description(self):
        percent = Smite.multiplier(self.level + 1) * 100.0
        return self.NextLevel.format(percent)
