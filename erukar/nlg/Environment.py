from .BaseNLG import BaseNLG

class Environment(BaseNLG):
    def describe_area_visually(observer, acu, sen, world, area):
        potentially_spotted = set()
        # Add all that we saw to our fog of war
        for coord in area:
            for actor in world.actors_at(observer, coord):
                potentially_spotted.add(actor)

        if not potentially_spotted:
            return 'Nothing catches your eye.'
        return 'You see ' + ', '.join([x.alias() for x in potentially_spotted])
