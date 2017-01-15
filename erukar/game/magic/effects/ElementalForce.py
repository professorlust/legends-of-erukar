from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation

class ElementalForce(ElementalAugmentation):
    DamageName = 'divine'
    DamageDescription = "{alias|target}'s body is shocked by a concussive force!"

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']

    PotionName = 'Force'
    PotionPriceMultiplier = 3.5
