from erukar.nlg.enum import *
from erukar.nlg.BaseNLG import BaseNLG
from erukar.nlg.base.SentenceStructure import SentenceStructure

class Sentence:
    def __init__(self):
        self.tense = Tense.SimplePresent
        self.verb = None

    def create(self, subj, obj):
        payload = {
            'subject': subj.formatted_alias(),
            'object': obj.formatted_alias(),
            'verb': getattr(self.verb, subj.verb_form_for())(self.tense)
        }

        return SentenceStructure.create(payload)
