from erukar.engine.lifeforms.Lifeform import Lifeform
import random, erukar

class Enemy(Lifeform):
    def perform_turn(self):
        targets = list(self.viable_targets())
        if len(targets) == 0:
            return
        target = random.choice(targets)

        roll, ac, damage = self.attack(target) 
        print_args = {
            'self': self.alias(),
            'target': target.alias(),
            'ac': ac,
            'roll': roll,
            'damage': damage}
        if roll <= ac:
            print('{self} tries to attack {target}, but misses ({ac} AC vs {roll})'.format(**print_args))
        if roll > ac:
            print('{self} hits {target} with an attack, dealing {damage} damage'.format(**print_args))

    def viable_targets(self):
        for item in self.current_room.contents:
            if isinstance(item, erukar.engine.lifeforms.Lifeform):
                if item is not self:
                    yield item
