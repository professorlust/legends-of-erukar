from erukar.engine.model.SpellEffect import SpellEffect

class BeginConjurationSequence(SpellEffect):
    '''
    Conjuration mechanics are a bit more complex than normal casting. They begin as such...

    <Modifiers> <BeginConjurationSequence> <Item or Creature Name> <EndConjurationSequence>

    This means that you can explicitly define in between the Begin/End what you want to summon.
    On a match failure the spell fizzles, so beware.
    '''
    pass
