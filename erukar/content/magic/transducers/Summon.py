from erukar.system.engine import Transducer, SummonAI
from erukar.content import Skeleton
from erukar.ext.math import Distance
import random


class Summon(Transducer):
    YouSummoned = 'The room grows colder as darkness flows from your '\
        'fingertips. Bones float and assemble into a skeleton under '\
        'your employ. It raises its sword and bows its head in '\
        'deferrence, ready to serve you!'

    def transduce(self, instigator, target, cmd, mutator):
        summon = mutator.get('creature_class', Skeleton)()
        random_location = self.get_summon_location(instigator, cmd, mutator)
        cmd.added_characters.append(summon)
        cmd.world.add_actor(summon, random_location)
        summon.ai_module = SummonAI(summon, instigator)
        summon.name = 'Summoned Skeleton'
        cmd.log(instigator, self.YouSummoned)
        return mutator

    def get_summon_type(self, **kwargs):
        return Skeleton

    def get_summon_location(self, instigator, cmd, mutator):
        return random.choice(list(Distance.direct_los(
            instigator.coordinates,
            cmd.world.all_traversable_coordinates(),
            max_distance=2)))
