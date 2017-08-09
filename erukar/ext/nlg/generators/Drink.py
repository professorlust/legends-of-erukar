from erukar.ext.nlg import Qualities, NlgObject, RegularVerb, BaseNLG, Sentence
import random

class Drink(BaseNLG):
    ActionVerbs = [
        (RegularVerb, 'chug'),
        (RegularVerb, 'drink'),
        (RegularVerb, 'down'),
        (RegularVerb, 'swallow')
    ]

    def taste(observer, acu, sen, item):
        you = NlgObject(observer.alias(), qualities=[Qualities.Observer])
        drink = NlgObject(item.alias())
        verb_type, verb_word = random.choice(Drink.ActionVerbs)
        s = Sentence(verb=verb_type(verb_word))
        return s.create(you, [drink])
