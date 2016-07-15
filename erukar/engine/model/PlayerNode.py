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
        if self.character in self.character.current_room.contents:
            self.character.current_room.contents.remove(self.character)
        self.character.link_to_room(room)
        if room.coordinates not in self.dungeon_map:
            self.dungeon_map[room.coordinates] = room
