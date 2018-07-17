from .BasicAI import BasicAI
from erukar.system.engine import Dead


class SummonAI(BasicAI):
    MaxDistanceFromOwner = 4

    def __init__(self, puppet, owner):
        super().__init__(puppet)
        self.owner = owner
        self.puppet.faction = self.owner.faction
        self.on_start(owner.world)
        self.owner.detected_entities.add(self)

    def perform_turn(self):
        '''
        Check to see if we need to heal our owner and can do so
        Check to see if we can buff our owner, and do so if we can
        Check to see if there are enemies of our owner, attack if so
        '''
        if self.is_owner_dead():
            return self.idle()
        if self.should_revive_owner():
            return self.revive_owner()
        if self.is_too_far_from_owner():
            return self.move_to_owner()
        return super().perform_turn()

    def is_owner_dead(self):
        return self.owner is None or self.owner.has_condition(Dead)

    def should_revive_owner(self):
        return False

    def revive_owner(self):
        pass

    def is_too_far_from_owner(self):
        path = self.get_path_to(self.owner.coordinates)
        return len(path) > self.MaxDistanceFromOwner

    def move_to_owner(self):
        coord = self.coordinate_nearest_to_owner()
        if coord == self.puppet.coordinates:
            return self.wait()
        return self.move(coord)

    def coordinate_nearest_to_owner(self):
        path = self.get_path_to(self.owner.coordinates)
        max_speed = self.max_move_speed()
        if len(path) > max_speed:
            return path[max_speed - 1]
        if len(path) < int(self.MaxDistanceFromOwner/2):
            return self.puppet.coordinates
        return path[-1 - int(self.MaxDistanceFromOwner/2)]
