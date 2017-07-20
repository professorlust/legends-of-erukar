from .BaseNLG import BaseNLG
from erukar.engine.calculators.Distance import Distance

class Environment(BaseNLG):
    def describe_area(observer, world, at):
        acu, sen = observer.get_detection_pair()
        return Environment.describe_area_visually(observer, world, at, acu)

    def describe_area_visually(observer, world, at, acu):
        inspected_coordinates = list(Distance.direct_los(observer.coordinates,
            world.all_traversable_coordinates(), 2*observer.visual_fog_of_war(), centered_on=at, radius_around=5))

        # Add all that we saw to our fog of war
        for seen in inspected_coordinates:
            observer.zones.all_seen.add(seen)

        return 'Things'
