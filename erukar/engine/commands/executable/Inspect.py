from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Containable import Containable
import random, math, erukar

class Inspect(ActionCommand):
    not_found = "Nothing matching '{0}' was found in this room."
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."

    TrackedParameters = ['target']
    aliases = ['inspect', 'look', 'search']

    def __init__(self):
        super().__init__()

    def execute(self):
        player = self.find_player()
        self.room = player.lifeform().current_room

        self.acuity, self.sense = [math.floor(random.uniform(*player.lifeform().stat_random_range(x))) for x in ('acuity', 'sense')]

        # Index in the player's active indexing tree
        self.index(self.room, player)
        failure = self.check_for_arguments()
        if failure: return failure

        # Check to see if we're directionally inspecting
        if isinstance(self.target, erukar.engine.model.Direction):
            return self.directional_inspect()
        return self.item_inspect()

    def item_inspect(self):
        result = self.target.on_inspect(self.find_player().lifeform(), self.acuity, self.sense)
        self.player.index_container(self.target)
        self.append_result(self.sender_uid, result)
        return self.succeed()

    def directional_inspect(self):
        result = self.room.directional_inspect(self.target, self.find_player().lifeform())
        self.append_result(self.sender_uid, result)
        return self.succeed()

    def resolve_target(self, opt_payload=''):
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self) and hasattr(self.context, 'target'):
            self.target = getattr(self.context, 'target')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'target') and self.target: return

        direction = self.determine_direction(opt_payload.lower())
        if direction:
            self.target = direction
            return

        if opt_payload is '':
            self.target = self.room
            return

        additionals = {
            'room': self.room,
            'floor': self.room.floor,
            'ceiling': self.room.ceiling
        }
        failure_object = self.find_in_target(opt_payload, self.room, 'target', additionals)
        return failure_object

    def index(self, container, player):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        if issubclass(type(container), Containable):
            for i in container.contents:
                player.index_item(i, container)
