from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Indexer import Indexer
import random, erukar, string

class Enemy(Lifeform, Indexer):
    def __init__(self, name=""):
        Indexer.__init__(self)
        Lifeform.__init__(self, name)
        
        chars = string.ascii_uppercase + string.digits
        self.uid = ''.join(random.choice(chars) for x in range(128))

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.do_attack(targets)
        return self.maybe_move_somewhere()

    def maybe_move_somewhere(self):
        for room_dir in list(self.current_room.adjacent_rooms()):
            room = self.current_room.get_in_direction(room_dir).room
            targets = list(self.viable_targets(room))
            if len(targets) > 0:
                return self.do_move(room_dir)

    def do_move(self, direction):
        m = erukar.engine.commands.executable.Move()
        m.sender_uid = self.uid
        m.payload = direction.name
        return m

    def do_attack(self, targets):
        target = random.choice(targets)
        a = erukar.engine.commands.executable.Attack()
        a.sender_uid = self.uid
        a.payload = target.alias()
        return a

    def viable_targets(self, room):
        for item in room.contents:
            # A player should always be in this list
            if isinstance(item, erukar.engine.lifeforms.Player):
                yield item

            # If you have sense < -2, you might attack inanimate objects...
            if self.sense <= -2 or isinstance(item, erukar.engine.lifeforms.Lifeform):
                # If you have sense < -3, you might attack other enemies
                if self.sense > -3 and not isinstance(item, erukar.engine.lifeforms.Player):
                    continue
                # If you have sense < -4, you might attack yourself on accident 
                if self.sense <= -4 or item is not self:
                    yield item
