from erukar.nlg.enum.Tense import Tense
from erukar.nlg.base.Verb import Verb

class ToBe(Verb):
    Conjugation = {
        'first': {
            Tense.SimplePresent: 'am',
            Tense.SimplePast: 'was',
            Tense.SimpleFuture: 'will be',
        },
        'second': {
            Tense.SimplePresent: 'are',
            Tense.SimplePast: 'were',
            Tense.SimpleFuture: 'will be',
        },
        'third': {
            Tense.SimplePresent: 'is',
            Tense.SimplePast: 'was',
            Tense.SimpleFuture: 'will be',
        },
        'plural': {
            Tense.SimplePresent: 'are',
            Tense.SimplePast: 'were',
            Tense.SimpleFuture: 'will be',
        }
    }
