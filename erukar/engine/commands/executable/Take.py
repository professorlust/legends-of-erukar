from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Item import Item

class Take(ActionCommand):
    NotFound = "Take target was not found"
    CannotTake = "'{}' cannot be taken."
    success = "Successfully took {0}"
    LimitToLocal = True
    SearchTargetMustBeIndexed = True

    '''
    requires:
        interaction_target
    '''

    def cost_to_take(self):    
        '''For the future -- should cost nothing for small objects, and many points for larger objects'''
        return 1

    def perform(self):
        if not self.args['interaction_target']: return self.fail(Take.NotFound)

        # Check to see if there are a sufficient number of Action Points available
        cost = self.cost_to_take()
        if self.args['player_lifeform'].action_points < cost:
            return self.fail('Not enough action points!')

        # Can the object be taken?
        if not issubclass(type(self.args['interaction_target']), Item):
            return self.fail('Cannot take this object')
        
        self.move_to_inventory()
        return self.succeed()

    def move_to_inventory(self):
        # We found it, so give it to the player and return a success msg
        self.args['player_lifeform'].inventory.append(self.args['interaction_target'])
        container = self.player_info.index(self.args['interaction_target'])
        self.player_info.remove_index(self.args['interaction_target'])
        if len(container) > 0:
            container[-1].remove(self.args['interaction_target'])

        take_result = self.args['interaction_target'].on_take(self.args['player_lifeform'])
        if take_result: self.append_result(self.player_info.uuid, take_result)

        self.dirty(self.args['player_lifeform'])
        self.append_result(self.player_info.uuid, Take.success.format(self.args['interaction_target'].describe()))
