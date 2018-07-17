from erukar.system.engine import Transducer, Aura


class CreateSanctityAura(Transducer):
    def transduce(self, instigator, target, cmd, mutator):
        '''Expects target to be a coordinate'''
        location = mutator.get('location', target.coordinates)
        sanctity = mutator.get('sanctity', 0.0)
        radius = CreateSanctityAura.radius(mutator.power())
        self.aura = Aura(location, sanctity, radius)
        self.aura.initiator = instigator
        self.aura.blocked_by_walls = False
        self.aura.modify_sanctity = self.modify_sanctity
        self.aura.world = instigator.world
        instigator.world.initiate_aura(self.aura, instigator.coordinates)
        cmd.log(instigator, CreateSanctityAura.result_string(sanctity))
        return mutator

    def modify_sanctity(self, loc):
        if not hasattr(self, 'aura') or not self.aura:
            return 0
        return self.aura.strength_at(loc)

    def radius(power):
        return int(power)
