from erukar.server.Instance import Instance
import erukar
from erukar.engine.environment import *
from erukar.engine.model.Direction import Direction

class HubInstance(Instance):
    def activate(self, action_commands, non_action_commands, joins, generation_parameters):
        self.dungeon = Dungeon()
        r1 = Room(self.dungeon, (0,0))
        r1.SelfDescription = 'This room is ornately built.'
        r2 = Room(self.dungeon, (0,1))
        r2.SelfDescription = 'This is the Kingspath Street.'
        r1.coestablish_connection(Direction.North, r2)
        super().activate(action_commands, non_action_commands, joins, generation_parameters)

    def decorate(self, generation_parameters):
        decorators = list(RandomDungeonInstance.decorators(generation_parameters))
        self.generation_parameters = generation_parameters
        # First Pass -- Actually add Decorations
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)
        # Second pass -- Tell Decorators to start
        for room in self.dungeon.rooms:
            room.on_start()

    def decorators(gen_params):
        for sm in RandomDungeonInstance.SubModules:
            md = sm[0](RandomDungeonInstance.BaseModule.format(sm[1]), gen_params)
            md.initialize()
            yield md


