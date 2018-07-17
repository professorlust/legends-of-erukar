from erukar.system.engine import Selector, Lifeform


class RadialArea(Selector):
    def applicable_targets(self, caster, cmd, mutator):
        origin = mutator.get('origin', caster.coordinates)
        radius = mutator.get('radius', 3)
        for actor in cmd.world.actors_in_range_los(caster, origin, radius):
            if not isinstance(actor, Lifeform):
                continue
            if actor.is_hostile_to(caster):
                yield actor
