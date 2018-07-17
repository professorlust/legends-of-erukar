from erukar.system.engine import Item
from ..ActionCommand import ActionCommand
from ..auto.Inventory import Inventory


class Take(ActionCommand):
    NotFound = "Take target was not found"
    CannotTake = "'{}' cannot be taken."
    success = "Successfully took {0}"
    LimitToLocal = True
    SearchTargetMustBeIndexed = False

    '''
    requires:
        interaction_target
    '''

    def cost_to_take(self):
        return 1

    def perform(self):
        target = self.args.get('interaction_target', None)
        if not target:
            return self.fail(Take.NotFound)

        # Can the object be taken?
        if not isinstance(target, Item):
            return self.fail('Cannot take this object')

        # Check to see if there are a sufficient number of Action Points
        player = self.args.get('player_lifeform')
        cost = self.cost_to_take()
        if player.action_points() < cost:
            return self.fail('Not enough action points!')

        player.consume_action_points(cost)

        self.move_to_inventory(player, target)
        return self.succeed()

    def move_to_inventory(self, player, target):
        # We found it, so give it to the player and return a success msg
        player.inventory.append(target)
        payload = Inventory.format_item(target, player)
        self.add_to_outbox(player, 'add item', payload)
        container = self.player_info.get_parent(target)
        self.player_info.remove_index(target)
        self.world.remove_actor(target)
        if container:
            container.remove(target)

        target.on_take(self)

        self.dirty(player)
        self.log(player, Take.success.format(target.describe()))
