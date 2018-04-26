from erukar.system.engine import StackableItem
from erukar.ext.nlg import Drink
import erukar

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
        base_description = Drink.taste(observer, *observer.get_detection_pair(), self)
        return ' '.join([base_description] + list(self.apply_effects(observer)))

    def apply_effects(self, instigator):
        for effect in self.effects:
            instance = effect()
            if isinstance(instance, erukar.system.engine.MagicEffect):
                yield instance.enact(instigator, instigator, **self.get_kwargs(effect))

    def get_kwargs(self, effect_type):
        return {}
