from erukar.game.magic.words.base.ElementalAugmentation import ElementalAugmentation

class Force(ElementalAugmentation):
    DamageName = 'force'
    DamageDescription = "{alias|target}'s body is shocked by a concussive force!"
    AugmentationType = 'Swift'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription', 'AugmentationType']

    PotionName = 'Force'
    PotionPriceMultiplier = 3.5
