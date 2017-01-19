from erukar.engine.model.SpellEffect import SpellEffect

class ArcaneAdeptAugmentation(SpellEffect):
    DamageShouldScale = True
    DamageScalar = 3

    PotionName = 'Adept'
    PotionPriceMultiplier = 30.0

    ParametersWhichShouldBeOverridden = ['DamageShouldScale', 'DamageScalar']
