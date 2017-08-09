from ..enum.Tense import Tense
from .SentenceStructure import SentenceStructure
from .BaseNLG import BaseNLG

class Sentence:
    def __init__(self, verb=None):
        self.tense = Tense.SimplePresent
        self.verb = verb

    def create(self, subj, objects):
        payload = {
            'subject': subj.formatted_alias(),
            'object': BaseNLG.join([obj.formatted_alias() for obj in objects]),
            'verb': getattr(self.verb, subj.verb_form_for())(self.tense)
        }

        return SentenceStructure.create(payload)
