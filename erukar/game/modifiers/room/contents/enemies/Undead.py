from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import erukar

class Undead(RoomModifier):
    Probability = 4
    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.enemies.undead', None)
        undead = randomizer.create_one()
        undead.link_to_room(room)
