from erukar.engine.inventory.Item import Item

class Torch(Item):
    Persistent = True
    BaseName = "Torch"
    EssentialPart = "tip"
    SupportPart = "handle"
    BriefDescription = "a torch"

    def __init__(self):
        super().__init__("Torch", "Torch")
        self.equipment_locations = ['left', 'right']
        self.name = "Torch"

    def on_inventory(self):
        return self.name

