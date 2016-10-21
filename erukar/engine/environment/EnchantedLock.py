from erukar.engine.environment.Lock import Lock

class EnchantedLock(Lock):
    OnUnlockString = 'The enchantment on the {alias} disappears!'

    def __init__(self, phrase):
        super().__init__()
        self.passphrase = phrase

    def on_hear(self, sound, decay=1.0, instigator=None, direction=None):
        if isinstance(sound, str):
            if self.passphrase.lower() in sound.lower():
                self.is_locked = False
                return self.OnUnlockString
        return ''

    def on_attack(self, *_):
        return ''
