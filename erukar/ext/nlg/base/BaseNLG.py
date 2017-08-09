class BaseNLG:
    def a_or_an(string):
        return 'an' if BaseNLG.word_begins_with_vowel(string) else 'a'

    def word_begins_with_vowel(string):
        return string[0].lower() in ['a', 'e', 'i', 'o', 'u', 'y']

    def word_ends_in_char(string, char):
        return string[-1].lower() == char

    def indefinite_article(subj, with_space=False):
        return 'the' if subj.is_plural() else BaseNLG.a_or_an(subj.alias)

    def join(words):
        if len(words) == 1: return words[0]
        if len(words) == 2: return ' and '.join(words)

        # add 'and ' as prefix to last word
        words[-1] = 'and ' + words[-1]
        return ', '.join(words)
