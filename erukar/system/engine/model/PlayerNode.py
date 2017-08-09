from .Indexer import Indexer

'''
The Player Node is maintained on the 
'''

class PlayerNode(Indexer):
    Disconnected       =-1  # Default State
    Idle               = 0  # When the player is in menus
    SelectingCharacter = 1
    CreatingCharacter  = 2
    SelectingRegion    = 3
    Playing            = 4  # When the player has chosen a character and is playing it

    def __init__(self, uid, world, character=None):
        super().__init__()
        self.status = PlayerNode.Disconnected
        self.uid = uid
        self.character = character
        self.dungeon_map = {}
        self.world = world
        self.emit = None
        self.sid = None
        self.tile_set_version = 0

    def create_command(self, cmd_type):
        cmd = cmd_type()
        cmd.world = self.world
        cmd.player_info = self
        return cmd

    def turn_modifier(self):
        return self.character.turn_modifier()

    def move_to_room(self, room):
        for coordinates in room.coordinates:
            self.dungeon_map[coordinates] = room

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

    def tell(self, msg_type, msg):
        if self.emit and self.sid:
            self.emit(msg_type, msg, room=self.sid)

    def update_socket(self, connection):
        self.emit = connection.emit
        self.sid = connection.sid
