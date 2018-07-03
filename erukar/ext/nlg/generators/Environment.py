from erukar.ext.nlg import Qualities, NlgObject, RegularVerb, BaseNLG, Sentence

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
        you = NlgObject(observer.alias(), qualities=[Qualities.Observer])
        s = Sentence(verb=RegularVerb('see'))
        return s.create(you, list(Environment.describe_actors_if_spotted(observer, acu, sen, potentially_spotted)))

    def describe_actors_if_spotted(observer, acu, sen, potentially_spotted):
        nlg_objects = list(Environment.get_detected_nlg_objects(observer, acu, sen, potentially_spotted))
        unique_aliases = list(set(nlg_objects))
        for alias in unique_aliases:
            count = len([x for x in nlg_objects if x == alias])
            qualities = [Qualities.Numeric] if count > 1 else []
            yield NlgObject(alias, count=count, qualities=qualities)

    def get_detected_nlg_objects(observer, acu, sen, potentially_spotted):
        for actor in potentially_spotted:
            if actor.is_detected(acu, sen):
                yield Environment.describe_actor(observer, actor, acu, sen)

    def describe_actor(observer, actor, acu, sen):
        return actor.alias()
