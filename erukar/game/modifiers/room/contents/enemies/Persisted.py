from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.lifeforms.Enemy import Enemy
import erukar

class Persisted(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        e = Enemy()
        print('Persisted')
        e.request_persisted_enemy()
        e.link_to_room(room)

