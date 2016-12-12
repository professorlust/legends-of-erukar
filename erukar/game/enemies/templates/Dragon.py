from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class Dragon(Enemy):
    def __init__(self, actual_name):
        super().__init__(actual_name)
        self.strength   = int(random.uniform(6, 8))
        self.dexterity  = int(random.uniform(3, 8))
        self.vitality   = int(random.uniform(6, 9))
        self.acuity     = int(random.uniform(4, 9))
        self.sense      = int(random.uniform(4, 9))
        self.resolve    = int(random.uniform(10, 13))
        self.name = actual_name

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.use_breath(targets[0])
        return self.maybe_move_somewhere()

    def use_breath(self, target):
        cast = erukar.engine.commands.executable.Cast()
        cast.sender_uid = self.uid
        cast.user_specified_payload = 'Breath on {}'.format(target.alias())
        return cast