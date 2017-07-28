class Verb:
    Conjugation = {}

    def first(self, tense):
        return self.get_conjugation_for_form('first').get(tense, '')

    def second(self, tense):
        return self.get_conjugation_for_form('second').get(tense, '')

    def third(self, tense):
        return self.get_conjugation_for_form('third').get(tense, '')

    def plural(self, tense):
        return self.get_conjugation_for_form('plural').get(tense, '')

    def get_conjugation_for_form(self, form):
        return self.Conjugation.get(form, {})
