from erukar.engine.model.Spell import Spell
import erukar

class Disorient(Spell):
    YouCastSpell = 'You say a few words in ancient Canthric, "Ul ghazha reyduul."'
    TheyCastSpell = '{alias|caster} speaks some words in an ancient language, then closes his eyes.'

    def __init__(self):
        super().__init__('Disorient',[
            erukar.game.magic.effects.ConditionBlinded(),
            erukar.game.magic.effects.InflictCondition()
        ])
