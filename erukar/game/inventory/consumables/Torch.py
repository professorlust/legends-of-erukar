from erukar.engine.inventory.Item import Item
import random, math

class Torch(Item):
    Persistent = True
    BaseName = "Torch"
    EssentialPart = "tip"
    SupportPart = "handle"
    BriefDescription = "a torch"
    PersistentAttributes = ['fuel']

    def __init__(self):
        super().__init__("Torch", "Torch")
        self.equipment_locations = ['left', 'right']
        self.fuel = random.uniform(0,100)
        self.name = "Torch"

    def on_inventory(self):
        return self.name

    def tick(self):
        if self.aura is not None:
            self.fuel -= 1
