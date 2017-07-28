from erukar.nlg.enum.SubjectQualities import SubjectQualities
from erukar.nlg.BaseNLG import BaseNLG

class NlgObject:
    def __init__(self, alias, count, qualities=None):
        self.alias = alias
        self.is_observer = False
        self.is_definite = False
        self.is_proper = False
        self.assign_qualities(qualities)
        self.count = count

    def assign_qualities(self, qualities):
        if not qualities: return
        self.is_observer = SubjectQualities.Observer in qualities
        self.is_definite = SubjectQualities.Definite in qualities
        self.is_proper   = SubjectQualities.Proper   in qualities

    def is_plural(self):
        return self.count > 1

    def verb_form_for(self):
        if self.is_observer: return 'second'
        if self.is_plural(): return 'plural'
        return 'third'

    def formatted_alias(self):
        if self.is_observer: return 'you'
        if self.is_proper: return self.alias
        if self.is_definite: return 'the ' + self.alias
        return ' '.join([BaseNLG.indefinite_article(self), self.alias])
