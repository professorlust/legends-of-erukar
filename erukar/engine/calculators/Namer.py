import random

class Namer:
    GutturalSyllables = [
        'ik',
        'ek',
        'ick',
        'eck',
        'ook',
        'ock'
        'og',
    ]

    FlowingConsonants = ['c', 'ch', 'd', 'dt', 'th', 'h', 'l', 'm', 'n', 'nm', 'ph', 'v', 'r', 'w']
    FlowingVowels = ['a', 'ae', 'e', 'ei', 'i', 'y', 'ou', 'u', 'iu']

    def random_flowing():
        syllables = []
        num_syllables = int(random.uniform(2, 4))
        for _ in range(num_syllables):
            syllables.append(''.join([random.choice(Namer.FlowingConsonants), random.choice(Namer.FlowingVowels)]))
        if random.random() > 0.4:
            syllables.insert(0, random.choice(Namer.FlowingVowels))
        return ''.join(syllables).capitalize()
