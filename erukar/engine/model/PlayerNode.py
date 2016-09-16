from erukar.engine.model.Indexer import Indexer

class PlayerNode(Indexer):
    def __init__(self, uid, character=None):
        super().__init__()
        self.uid = uid
        self.character = character
        self.dungeon_map = {}

    def turn_modifier(self):
        return self.character.turn_modifier()

    def move_to_room(self, room):
        if room.coordinates not in self.dungeon_map:
            self.dungeon_map[room.coordinates] = room

    def afflicted_with(self, type_of):
        if self.character is None: return False

        return self.character.afflicted_with(type_of)

    def begin_turn(self):
        if self.character is not None:
            return self.character.begin_turn()
        return ''

    def end_turn(self):
        if self.character is not None:
            return self.character.end_turn()
        return ''

    def is_incapacitated(self):
        if self.character is not None:
            return self.character.is_incapacitated()
        return True

    def lifeform(self):
        return self.character
