from .ItemModifier import ItemModifier
from erukar.system.engine import Aura, Observation, Dungeon, Lifeform


class AuraModifier(ItemModifier):
    AuraDescription = "Aura"
    SelfAuraDescription = "This is your Aura"

    Glances = [
    ]

    def apply_to(self, item):
        super().apply_to(item)
        self.aura = None
        self.max_distance = 4
        self.power = 1.0

    def on_start(self, dungeon):
        self.start_aura(dungeon)

    def on_take(self, lifeform):
        self.stop_aura()

    def on_drop(self, world):
        self.start_aura(world)

    def on_move(self, coords):
        if self.aura:
            self.aura.move(coords)

    def on_equip(self, lifeform):
        self.start_aura(lifeform)

    def start_aura(self, initiator):
        self.aura = Aura((0, 0), self.power, self.max_distance)
        self.aura.Glances = self.Glances
        self.aura.initiator = initiator
        self.aura.blocked_by_walls = True
        self.modify_aura()
        if isinstance(initiator, Dungeon):
            self.aura.world = initiator
            initiator.initiate_aura(self.aura, self.applied_to.coordinates)
        if isinstance(initiator, Lifeform):
            self.aura.world = initiator.world
            initiator.world.initiate_aura(self.aura, initiator.coordinates)

    def modify_aura(self):
        pass

    def on_unequip(self, lifeform):
        self.stop_aura()

    def stop_aura(self):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None
