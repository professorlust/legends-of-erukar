from .BaseNLG import BaseNLG
from ..enum import Qualities

class NlgObject:
    def __init__(self, alias, count=1, qualities=None):
        self.alias = alias
        self.is_observer = False
        self.is_definite = False
        self.is_proper = False
        self.is_numeric = False
        self.assign_qualities(qualities)
        self.count = count

    def assign_qualities(self, qualities):
        if not qualities: return
        self.is_observer = Qualities.Observer in qualities
        self.is_definite = Qualities.Definite in qualities
        self.is_proper   = Qualities.Proper   in qualities
        self.is_numeric  = Qualities.Numeric  in qualities

    def is_plural(self):
        return self.count > 1

    def verb_form_for(self):
        if self.is_observer: return 'second'
        if self.is_plural(): return 'plural'
        return 'third'

    def formatted_alias(self):
        if self.is_observer: return 'you'
        if self.is_proper:   return self.alias
        if self.is_numeric:  return ' '.join([str(self.count), self.alias])
        if self.is_definite: return 'the ' + self.alias
        return ' '.join([BaseNLG.indefinite_article(self), self.alias])
