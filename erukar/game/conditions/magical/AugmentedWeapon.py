from erukar.engine.model.Affliction import Affliction
import erukar

class AugmentedWeapon(Affliction):
    Duration = 12 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def __init__(self, afflicted):
        super().__init__(afflicted)
        self.timer = AugmentedWeapon.Duration
        self.weapon = None
        self.modifier = None
        self.augment_weapon(afflicted)

    def tick(self):
        self.timer -= 1
        if self.timer <= 0:
            self.exit()

    def augment_weapon(self, afflicted):
        for slot in afflicted.attack_slots:
            self.weapon = getattr(afflicted, slot)
            if self.weapon is not None and isinstance(self.weapon, erukar.engine.inventory.Weapon):
                self.modifier = erukar.game.modifiers.inventory.random.Flaming()
                self.modifier.persistent = False
                self.modifier.apply_to(self.weapon)
                return

    def exit(self):
        self.modifier.remove()
        self.afflicted.afflictions.remove(self)
