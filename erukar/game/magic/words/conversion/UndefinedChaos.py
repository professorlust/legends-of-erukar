from erukar.engine.magic.SpellWord import SpellWord

class UndefinedChaos(SpellWord):
    '''
    This is used when the caster does not specify a conversion word.
    
    Likelihood  | Outcome
    ------------|---------
    49%         | Nothing (Fizzle)
    12.5%       | Light
    12.5%       | Smoke
    12.5%       | Noise 
    12.5%       | Convert Source to Environment
    0.40%       | Explosion
    0.40%       | Heal
    0.10%       | Greater Explosion
    0.10%       | Greater Heal
    '''
    pass
