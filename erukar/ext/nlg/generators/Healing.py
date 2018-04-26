from erukar.ext.nlg import Qualities, NlgObject, RegularVerb, BaseNLG, Sentence
import random

class Healing(BaseNLG):
    QuantifiableVerbs = [
        (RegularVerb, 'gain'),
        (RegularVerb, 'heal'),
    ]

    def quantified(observer, amount, type):
        you = NlgObject(observer.alias(), qualities=[Qualities.Observer])
        gain = NlgObject(type, count=amount, qualities=[Qualities.Numeric])
        verb_type, verb_word = random.choice(Healing.QuantifiableVerbs)
        s = Sentence(verb=verb_type(verb_word))
        return s.create(you, [gain])

    def description(observer, acu, sen):
        pass
