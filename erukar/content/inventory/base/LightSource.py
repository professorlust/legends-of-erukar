from erukar.system.engine import Item, Aura, Observation, Dungeon, Lifeform
from erukar.ext.math import Curves
import random


class LightSource(Item):
    Persistent = True
    BaseName = "Light source"
    EssentialPart = "wick"
    SupportPart = "container"
    BriefDescription = "a source of light"
    SelfAuraDescription = "Your source of light brightens the room."
    AuraDescription = "A pale white glow shines through {relative_direction}."
    PersistentAttributes = ['fuel']
    EquipmentLocations = ['right', 'left']

    MaxFuel = 100
    FuelConsumptionRate = 0.25  # per five seconds
    StrengthAtMaxFuel = 1
    StrengthAtZeroFuel = 0.3
    DistanceAtMaxFuel = 0.5
    DistanceAtZeroFuel = 0.2

    Glances = [
        Observation(acuity=1, sense=1, result='Light flickers.')
    ]

    def __init__(self):
        super().__init__(self.BaseName, self.BaseName)
        self.aura = None
        self.equipment_locations = ['left', 'right']
        self.fuel = random.uniform(self.MaxFuel/2, self.MaxFuel)
        self.name = self.BaseName
        self.modifiers = []

    def on_inventory(self):
        return '{} ({}%)'.format(self.name, int(self.fuel))

    def on_inventory_inspect(self, lifeform):
        return '{}\n\t• {}% Fuel Remaining'.format(self.name, int(self.fuel))

    def tick(self):
        if self.aura is not None:
            self.fuel -= self.FuelConsumptionRate
            self.aura.aura_strength = self.strength()
            self.aura.max_distance = self.max_distance()
            if self.fuel <= 0:
                self.stop_aura()

    def on_start(self, dungeon):
        self.start_aura(dungeon)

    def on_take(self, lifeform):
        self.stop_aura()

    def on_drop(self, room, lifeform):
        self.start_aura(room)

    def on_move(self, *_):
        if self.aura:
            self.aura.move(self.aura.initiator.coordinates)

    def on_equip(self, lifeform):
        self.start_aura(lifeform)

    def on_unequip(self, lifeform):
        self.stop_aura()

    def modify_light(self, loc):
        if not self.aura:
            return 0
        return self.aura.strength_at(loc)

    def start_aura(self, initiator):
        if self.fuel <= 0:
            return
        self.aura = Aura((0, 0), self.strength(), self.max_distance())
        self.aura.Glances = self.Glances
        self.aura.initiator = initiator
        self.aura.blocked_by_walls = True
        self.aura.modify_light = self.modify_light
        if isinstance(initiator, Dungeon):
            self.aura.world = initiator
            initiator.initiate_aura(self.aura, self.coordinates)
        if isinstance(initiator, Lifeform):
            self.aura.world = initiator.world
            initiator.world.initiate_aura(self.aura, initiator.coordinates)

    def stop_aura(self):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None

    def strength(self):
        return Curves.dropoff(
            0,
            self.MaxFuel,
            self.StrengthAtZeroFuel,
            self.StrengthAtMaxFuel,
            self.fuel)

    def max_distance(self):
        return Curves.dropoff(
            0,
            self.MaxFuel,
            self.DistanceAtZeroFuel,
            self.DistanceAtMaxFuel,
            self.fuel)
