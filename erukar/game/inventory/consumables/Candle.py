from erukar.game.inventory.base.LightSource import LightSource
from erukar.engine.model.Observation import Observation

class Candle(LightSource):
    BaseName = "Candle"
    EssentialPart = "wick"
    SupportPart = "base"
    BriefDescription = "a candle"
    SelfAuraDescription = "The soft white light of the candle in your hand slightly illuminates the room."
    Glances = [
        Observation(acuity=1, sense=1, result='Soft light fills the room.')
    ]

    MaxFuel = 100
    FuelConsumptionRate = 0.1
    StrengthAtMaxFuel = 3.0
    StrengthAtZeroFuel = 1.0
    DecayAtMaxFuel = 0.5
    DecayAtZeroFuel = 0.3
