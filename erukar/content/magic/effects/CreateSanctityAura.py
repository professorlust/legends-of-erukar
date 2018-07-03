from erukar.system.engine import MagicEffect, Aura


class CreateSanctityAura(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        '''Expects target to be a coordinate'''
        location = instigator.coordinates
        location = CreateSanctityAura.arg('location', location, tuple, **kwargs)
        sanctity = CreateSanctityAura.arg('sanctity', 0.0, float, **kwargs)
        radius = CreateSanctityAura.arg('radius', 3.0, float, **kwargs)
        self.aura = Aura(location, sanctity, radius)
        self.aura.initiator = instigator
        self.aura.blocked_by_walls = False
        self.aura.modify_sanctity = self.modify_sanctity
        self.aura.world = instigator.world
        instigator.world.initiate_aura(self.aura, instigator.coordinates)
        if sanctity > 0:
            return 'The world becomes more pure.', kwargs
        if sanctity < 0:
            return 'The world becomes more unclean.', kwargs
        return 'Nothing happens...', kwargs

    def modify_sanctity(self, loc):
        if not hasattr(self, 'aura') or not self.aura:
            return 0
        return self.aura.strength_at(loc)
