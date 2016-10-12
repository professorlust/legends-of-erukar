from erukar.engine.model.Spell import Spell
import erukar

class ElectricBreath(Spell):
    YouCastSpell = "You breathe in deeply, then release a blast of sparks and arcs of lightning!"
    TheyCastSpell = "{alias|lifeform} breathes in deeply, then releases a blast of sparks and lightning!"

    def __init__(self):
        super().__init__('Electric Breath',[erukar.game.magic.effects.ElectricDamage()])



