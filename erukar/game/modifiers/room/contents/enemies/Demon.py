from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import erukar

class Demon(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.enemies.demon', None)
        undead = randomizer.create_one()
        undead.link_to_room(room)
