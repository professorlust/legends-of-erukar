from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import erukar

class Dragon(RoomModifier):
    Probability = 10
    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.enemies.dragon', None)
        undead = randomizer.create_one()
        undead.link_to_room(room)
