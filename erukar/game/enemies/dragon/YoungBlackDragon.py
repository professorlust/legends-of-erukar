from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class YoungBlackDragon(Enemy):
    BriefDescription = "a young Black Dragon"

    def __init__(self):
        super().__init__("Young Black Dragon")
        self.strength   = int(random.uniform(6, 8))
        self.dexterity  = int(random.uniform(3, 8))
        self.vitality   = int(random.uniform(6, 9))
        self.acuity     = int(random.uniform(4, 9))
        self.sense      = int(random.uniform(4, 9))
        self.resolve    = int(random.uniform(10, 13))
        self.spells = [erukar.game.magic.predefined.AcidBreath()]
        self.define_level(11)
        self.name = "Young Black Dragon"
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a Young Black Dragon.', 'There is a Young Black Dragon.')

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.use_breath(targets[0])
        return self.maybe_move_somewhere()

    def use_breath(self, target):
        cast = erukar.engine.commands.executable.Cast()
        cast.sender_uid = self.uid
        cast.user_specified_payload = 'Acid Breath on {}'.format(target.alias())
        return cast
