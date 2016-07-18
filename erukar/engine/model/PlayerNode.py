from erukar.engine.model.Indexer import Indexer

class PlayerNode(Indexer):
    def __init__(self, uid, character):
        super().__init__()
        self.uid = uid
        self.character = character
        self.dungeon_map = {}

    def turn_modifier(self):
        return self.character.turn_modifier()

    def move_to_room(self, room):
        if room.coordinates not in self.dungeon_map:
            self.dungeon_map[room.coordinates] = room
