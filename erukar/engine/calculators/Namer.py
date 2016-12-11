import random

class Namer:
    first_consonant = [
        '',
        'b',
        'c',
        'ch',
        'd',
        'f',
        'g',
        'h',
        'j',
        'k',
        'l',
        'm',
        'n',
        'p',
        'ph',
        'qu',
        'r',
        's',
        'sh',
        'st',
        'sk',
        't',
        'th',
        'v',
        'w',
        'z'
    ]

    vowel = [
        'a',
        'ae',
        'e',
        'i',
        'o',
        'ou',
        'u'
    ]

    trailing_consonant = [
        '',
        'b',
        'ch',
        'd',
        'ff',
        'g',
        'gh',
        'h',
        'k',
        'ck',
        'll',
        'm',
        'mn',
        'n',
        'p',
        'ph',
        'r',
        'rt',
        'rd',
        'rst',
        's',
        'ss',
        'sh',
        'st',
        'sk',
        't',
        'th',
        'v',
        'w',
        'z'
    ]


    def create_syllable():
        return random.choice(Namer.first_consonant) + random.choice(Namer.vowel) + random.choice(Namer.trailing_consonant) 

    def random_flowing():
        num_syllables = int(max(1.0, random.gauss(3,1)))
        syllables = []
        for index in range(num_syllables):
            syllables.append(Namer.create_syllable())
        return ''.join(syllables)

