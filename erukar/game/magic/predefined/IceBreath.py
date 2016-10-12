from erukar.engine.model.Spell import Spell
import erukar

class IceBreath(Spell):
    YouCastSpell = "You breathe in deeply, then release a blast of ice and incredibly cold air from your lungs!"
    TheyCastSpell = "{alias|lifeform} breathes in deeply, then releases a blast of ice and incredibly cold air from {gender_pronoun_possessive|lifeform}'s lungs!"

    def __init__(self):
        super().__init__('Ice Breath',[erukar.game.magic.effects.IceDamage()])
