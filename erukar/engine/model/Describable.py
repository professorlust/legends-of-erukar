from .Interactible import Interactible

class Describable(Interactible):
    def visual_description(self, lifeform, acuity):
        return ''

    def sensed_description(self, lifeform, sense):
        return ''

    def describe(self):
        pass

