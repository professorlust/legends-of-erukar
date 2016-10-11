from erukar.engine.inventory.Item import Item
from erukar.engine.environment.Aura import Aura
from erukar.engine.calculators.Curves import Curves
import erukar, random, math

class LightSource(Item):
    Persistent = True
    BaseName = "Light source"
    EssentialPart = "wick"
    SupportPart = "container"
    BriefDescription = "a source of light"
    SelfAuraDescription = "Your source of light brightens the room."
    AuraDescription = "A pale white glow shines through {relative_direction}."
    PersistentAttributes = ['fuel']
    EquipmentLocations = ['right','left']

    MaxFuel = 100
    FuelConsumptionRate = 0.25 # per five seconds
    StrengthAtMaxFuel = 3
    StrengthAtZeroFuel = 1
    DecayAtMaxFuel = 0.5
    DecayAtZeroFuel = 0.2

    def __init__(self):
        super().__init__(self.BaseName,self.BaseName)
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
            self.aura.decay_factor = self.decay_factor()
            if self.fuel <= 0:
                self.stop_aura()

    def on_start(self, room):
        self.start_aura(room)

    def on_take(self, lifeform):
        self.stop_aura()

    def on_drop(self, room, lifeform):
        self.start_aura(room)

    def on_move(self, room):
        if self.aura:
            self.aura.location = room

    def on_equip(self, lifeform):
        self.start_aura(lifeform)

    def on_unequip(self, lifeform):
        self.stop_aura()

    def modify_light(self, decay=1):
        return self.strength() * decay

    def start_aura(self, initiator):
        if self.fuel <= 0: return
        self.aura = Aura((0,0), self.strength(), self.decay_factor())
        self.aura.initiator = initiator
        self.aura.blocked_by_walls = True
        self.aura.modify_light = self.modify_light
        self.aura.BriefDescription = self.AuraDescription
        self.aura.SelfAuraDescription = self.SelfAuraDescription
        initiator.initiate_aura(self.aura)

    def stop_aura(self):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None

    def strength(self):
        return Curves.dropoff(0, self.MaxFuel, self.StrengthAtZeroFuel, self.StrengthAtMaxFuel, self.fuel)

    def decay_factor(self):
        return Curves.dropoff(0, self.MaxFuel, self.DecayAtZeroFuel, self.DecayAtMaxFuel, self.fuel)
