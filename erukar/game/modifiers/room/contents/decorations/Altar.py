from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random

class Altar(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 0.1
    ProbabilityFromSanctity = 1.0

    broad_alias_base = 'altar'

    deity_possibilities = [
        'the God Omanis',
        'the Goddess Crepascia',
        'the God Olevarde',
        'Lord Ravodin, Protector of the Light']

    def apply_to(self, room):
        deity = random.choice(self.deity_possibilities)
        direction = self.random_wall(room)

        # Create the Altar proper
        deco = Decoration(aliases=[self.broad_alias_base])
        deco.set_vision_results('You see an altar to the {} of the room.'.format(direction),'You see an altar to {} to the {} of the room.'.format(deity, direction), (1, 5))
        deco.set_sensory_results('You smell burning incense.','You can sense holiness from an altar nearby',(1, 10))
        deco.set_detailed_results('The smell of incense burning on an altar to {} fills the room. The altar is located on the {} wall.'.format(deity, direction),\
                                  'A warm smell of lightly burning incense on an altar to the {} fills the room with a sense of holiness. The presence of {} can be felt here, and it is evident that his acolytes have been incredibly loyal.'.format(direction,deity))
        self.create_altar_top(room)
        room.add(deco)

    def create_altar_top(self, room):
        top = Container(['top of the altar', 'altar top'])
        r = ModuleDecorator('erukar.game.inventory', self.generation_parameters)
        top.add(r.create_one())
