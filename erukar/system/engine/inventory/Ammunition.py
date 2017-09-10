from .StackableItem import StackableItem
import random

class Ammunition(StackableItem):
    BriefDescription = "Ammunition for a weapon"
    BaseName = "Ammunition"
    EquipmentLocations = ['ammunition']

    def __init__(self, quantity=1, modifiers=None):
        super().__init__(self.BaseName, modifiers=modifiers)
        self.quantity = quantity

    def on_calculate_attack(self, attack_state):
        for modifier in self.modifiers:
            modifier.on_calculate_attack_ranged(attack_state)

    def consume(self):
        self.quantity -= 1
        if self.quantity <= 0:
            self.owner.inventory.remove(self)
            self.owner.ammunition = None
