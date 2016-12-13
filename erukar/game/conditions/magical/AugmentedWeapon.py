from erukar.engine.model.Affliction import Affliction
import erukar

class AugmentedWeapon(Affliction):
    IsTemporary = True
    Duration = 12 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    MaxInstances = 1

    def __init__(self, afflicted, modifier_Type):
        super().__init__(afflicted)
        self.modifier_type = erukar.game.modifiers.inventory.random.Flaming
        self.timer = AugmentedWeapon.Duration
        self.weapon = None
        self.modifier_instances = []
        self.augment_weapon(afflicted)

    def tick(self):
        if self.IsTemporary:
            self.timer -= 1
            if self.timer <= 0:
                self.exit()

    def augment_weapon(self, afflicted):
        for slot in afflicted.attack_slots:
            self.weapon = getattr(afflicted, slot)
            if self.weapon is not None and isinstance(self.weapon, erukar.engine.inventory.Weapon):
                modifier = self.modifier_type()
                modifier.persistent = False
                modifier.apply_to(self.weapon)
                self.modifier_instances.append(modifier)
                if len(self.modifier_instances) >= self.MaxInstances:
                    return

    def exit(self):
        for modifier in self.modifier_instances:
            modifier.remove()
        self.afflicted.afflictions.remove(self)
