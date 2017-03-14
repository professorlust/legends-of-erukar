from erukar.engine.magic.SpellWord import SpellWord

class LogicWord(SpellWord):
    '''
    Logic Words are by far the most complicated spell words available to a wizard. They allow for 
    chunks of a spell word to operate multiple times or to have conditional looping. For instance,
    take the spell word chain...

        ArcaneSource, Fire, Concentrate, Bolt, Ice, Bolt
    
    The spell word chain will execute up until the first 'Bolt', where it will expend all of its 
    arcane energy. Thus, the Bolt of Ice will have no access to arcane energy and will fail. Now
    consider the usage of the Logic word "Split"...

        ArcaneSource, Split, Fire, Concentrate, Bolt, Ice, Bolt

    The 'Split' word indicates that there are to be multiple conversion words which will require
    arcane energy, and thus will provide equal sources of Arcane energy to the chain up until
    the first Bolt and then from there up until the second Bolt. Thus, using the same spell,
    we get two effective spells at half efficacy: [ArcaneSource, Fire, Concentrate, Bolt] and
    [ArcaneSource, Ice, Bolt].

    There are special Logic words which create what are known as Spell Folds. These are coupled
    in the following way:

        ArcaneSource, <Condition>, Fire, Bolt, EndFold, Ice, Bolt

    Condition, in this instance, is a unique logic word which does not consume any arcane energy
    and allows the spellcaster to indicate a very specific condition which would execute the 
    spell words within <Condition> and EndFold. There are many examples of <Condition>, such as
    TargetIsEthereal or TargetIsIncapacitated.

    An example of a Conditional Spell is the following.

        ArcaneSource, SelfIsBloodied, Split, Concentrate, HealingEffect, EndFold, Light

    The above spell checks to see if the caster is bloodied (health < 50%) and casts a concentrated
    healing effect if so. Either way, the spell creates light.
    '''
    pass
