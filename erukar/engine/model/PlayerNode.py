from erukar.engine.model.Indexer import Indexer

class PlayerNode(Indexer):
    Disconnected  =-1  # Default State
    Idle          = 0  # When the player is in menus
    PrePlaying    = 1  # When the player is in a tutorial or building character
    Playing       = 2  # When the player has chosen a character and is playing it
    RunningScript = 3

    def __init__(self, uid, character=None):
        super().__init__()
        self.status = PlayerNode.Disconnected
        self.uid = uid
        self.character = character
        self.dungeon_map = {}
        self.active_script = ''
        self.script_entry_point = None

    def turn_modifier(self):
        return self.character.turn_modifier()

    def move_to_room(self, room):
        if room.coordinates not in self.dungeon_map:
            self.dungeon_map[room.coordinates] = room

    def has_condition(self, type_of):
        if self.character is None: return False

        return self.character.has_condition(type_of)

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

    def run_script(self, script):
        self.active_script = script
        self.status = PlayerNode.RunningScript

    def set_script_entry_point(self, entry_point):
        self.script_entry_point = entry_point
