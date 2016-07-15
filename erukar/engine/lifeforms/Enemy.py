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
        targets = list(self.viable_targets())
        if len(targets) == 0:
            return
        target = random.choice(targets)
        a = erukar.engine.commands.executable.Attack()
        a.sender_uid = self.uid
        a.payload = target.alias()
        return a

    def viable_targets(self):
        for item in self.current_room.contents:
            if isinstance(item, erukar.engine.lifeforms.Lifeform):
                if item is not self:
                    yield item
