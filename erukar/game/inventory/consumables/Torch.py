from erukar.game.inventory.base.LightSource import LightSource
from erukar.engine.model.Observation import Observation

class Torch(LightSource):
    BaseName = "Torch"
    EssentialPart = "tip"
    SupportPart = "handle"
    BriefDescription = "a torch"
    SelfAuraDescription = "The light from your torch illuminates the room."
    AuraDescription = "The flickering, golden light of a torch flows into the room from {relative_direction}."
    Glances = [
        Observation(acuity=1, sense=1, result='Torchlight fills the room.')
    ]

    MaxFuel = 100
    FuelConsumptionRate = 0.3
    StrengthAtMaxFuel = 6.0
    StrengthAtZeroFuel = 2.0
    DecayAtMaxFuel = 0.75
    DecayAtZeroFuel = 0.2
