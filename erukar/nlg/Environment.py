from .BaseNLG import BaseNLG

class Environment(BaseNLG):
    SentenceStructures = [
        '{indef_sbj_article} {subject} {verb} {object}.',
        'The {subject} {verb} {object}.',
        'You see a {subject} which {verb} {object}'
    ]

    def describe_area_visually(observer, acu, sen, world, area):
        potentially_spotted = set()
        # Add all that we saw to our fog of war
        for coord in area:
            for actor in world.actors_at(observer, coord):
                potentially_spotted.add(actor)

        if not potentially_spotted:
            return 'Nothing catches your eye.'

        return ' '.join(Environment.describe_actors_if_spotted(observer, acu, sen, potentially_spotted))

    def describe_actors_if_spotted(observer, acu, sen, potentially_spotted):
        for actor in potentially_spotted:
            if actior.is_detected(acu, sen):
                yield Environment.describe_actor(observer, actor, acu, sen)

    def describe_actor(observer, actor, acu, sen):
        subject = actor.alias()
        indef_sbj_article = BaseNLG.a_or_an(subject)
