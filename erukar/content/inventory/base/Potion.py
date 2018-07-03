from erukar.system.engine import StackableItem, SpellInstance
from erukar.ext.nlg import Drink


class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    IsUsable = True
    BriefDescription = "a red potion"

    def __init__(self, quantity=1):
        super().__init__(self.BaseName, quantity)
        self.effects = []

    def duplication_args(self, quantity):
        return {
            'quantity': quantity,
        }

    def price(self, econ=None):
        return 10

    def on_use(self, observer):
        self.consume()
        acu, sen = observer.get_detection_pair()
        base_description = Drink.taste(observer, acu, sen, self)
        spell = SpellInstance(self.effects)
        log = spell.execute(observer, observer, **self.get_kwargs())
        return ' '.join([base_description] + list(log))

    def get_kwargs(self):
        return {}
