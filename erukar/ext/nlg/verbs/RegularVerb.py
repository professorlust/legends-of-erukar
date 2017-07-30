from erukar.ext.nlg import BaseNLG, Tense, Verb

class RegularVerb(Verb):
    Conjugation = {
        'first': {
            Tense.SimplePresent: '{}',
            Tense.SimplePast: '{}ed',
            Tense.SimpleFuture: 'will {}',
        },
        'second': {
            Tense.SimplePresent: '{}',
            Tense.SimplePast: '{}ed',
            Tense.SimpleFuture: 'will {}',
        },
        'third': {
            Tense.SimplePresent: '{}s',
            Tense.SimplePast: '{}ed',
            Tense.SimpleFuture: 'will {}',
        },
        'plural': {
            Tense.SimplePresent: '{}',
            Tense.SimplePast: '{}ed',
            Tense.SimpleFuture: 'will {}',
        }
    }

    def __init__(self, base):
        self.base = base

    def get_base(self, conjugation):
        _, suffix = conjugation.split('{}')
        if suffix and suffix[0].lower() == 'e' and self.ends_in_e():
            return self.base[:-1]
        return self.base

    def ends_in_e(self):
        return BaseNLG.word_ends_in_char(self.base, 'e')

    def first(self, tense):
        return self.get_form_and_conjugate('first', tense)

    def second(self, tense):
        return self.get_form_and_conjugate('second', tense)

    def third(self, tense):
        return self.get_form_and_conjugate('third', tense)

    def plural(self, tense):
        return self.get_form_and_conjugate('plural', tense)

    def get_form_and_conjugate(self, form, tense):
        conj = self.get_conjugation_for_form(form).get(tense, '')
        return conj.format(self.get_base(conj))

    def get_conjugation_for_form(self, form):
        return self.Conjugation.get(form, {})

