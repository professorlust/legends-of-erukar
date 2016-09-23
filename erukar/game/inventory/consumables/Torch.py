from erukar.engine.inventory.Item import Item
from erukar.engine.environment.Aura import Aura
from erukar.engine.calculators.Curves import Curves
import erukar, random, math

class Torch(Item):
    Persistent = True
    BaseName = "Torch"
    EssentialPart = "tip"
    SupportPart = "handle"
    BriefDescription = "a torch"
    AuraDescription = "The flickering, golden light of a torch flows into the room from {relative_direction}."
    PersistentAttributes = ['fuel']

    def __init__(self):
        super().__init__("Torch", "Torch")
        self.aura = None
        self.equipment_locations = ['left', 'right']
        self.fuel = random.uniform(50,100)
        self.name = "Torch"
        self.modifiers = []

    def on_inventory(self):
        return '{}\n\t• {}% Fuel Remaining'.format(self.name, int(self.fuel))

    def tick(self):
        if self.aura is not None:
            self.fuel -= 1
            self.aura.aura_strength = self.torch_strength()
            self.aura.decay_factor = self.decay_factor()
            if self.fuel <= 0:
                self.stop_aura()

    def on_start(self, room):
        self.start_aura(room)

    def on_take(self, lifeform):
        self.stop_aura()

    def on_drop(self, room, lifeform):
        self.start_aura(lifeform)

    def on_move(self, room):
        if self.aura:
            self.aura.location = room

    def on_equip(self, lifeform):
        self.start_aura(lifeform)

    def on_unequip(self, lifeform):
        self.stop_aura()

    def modify_light(self, decay=1):
        return self.torch_strength() * decay

    def start_aura(self, initiator):
        if self.fuel <= 0: return
        self.aura = Aura((0,0), self.torch_strength(), self.decay_factor())
        self.aura.initiator = initiator
        self.aura.blocked_by_walls = True
        self.aura.modify_light = self.modify_light
        self.aura.BriefDescription = self.AuraDescription
        initiator.initiate_aura(self.aura)

    def stop_aura(self):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None

    def torch_strength(self):
        return Curves.dropoff(0,100,2.0,6.0,self.fuel)

    def decay_factor(self):
        return Curves.dropoff(0, 100, 0.667, 0.25, self.fuel)
