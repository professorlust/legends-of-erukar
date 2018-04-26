from .Key import Key

class TieredKey(Key):
    MaximumStackQuantity = 9999
    Persistent = True
    BriefDescription = "a {Tier} key"
    WrongTarget = 'Invalid target for use with a {Tier} key.'
    FailedToUnlock = 'This lock is a {} tier; you cannot unlock it with a {} key.'
    Tier = 'Iron'

    def __init__(self):
        super().__init__('Key')

    def price(self, econ=None):
        return self.BasePrice
