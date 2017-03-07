from erukar.engine.magic.SpellWord import SpellWord

class Adept(SpellWord):
    DamageShouldScale = True
    DamageScalar = 3
    DamageOverTimeEfficacy = 1.5
    
    PotionName = 'Adept'
    PotionPriceMultiplier = 30.0

    ParametersWhichShouldBeOverridden = ['DamageShouldScale', 'DamageScalar', 'DamageOverTimeEfficacy']

    Name = 'Arcane Adept Effect'
    Description = '[!BUG] Automatically added due to the Arcane Adept Skill'
