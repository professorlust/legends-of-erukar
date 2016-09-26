from erukar.game.modifiers.RoomModifier import RoomModifier
import erukar

class Demon(RoomModifier):
    Probability = 0.02
    def apply_to(self, room):
        demon = erukar.game.enemies.demon.Cuadrodemon()
        demon.current_room = room
        room.add(demon)

