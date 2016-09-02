from .Interactible import Interactible

class Describable(Interactible):
    def __init__(self):
        self.vision_range = (0, 1)
        self.vision_minimal = 'Minimal Visual Result'
        self.vision_ideal = 'Ideal Visual Result'
        self.sense_range = (0, 1)
        self.sense_minimal = 'Minimal Sensory Result'
        self.sense_ideal = 'Ideal Sensory Result'

    def visual_description(self, lifeform, acuity):
        if acuity > self.vision_range[1]:
            return self.vision_ideal
        if acuity > self.vision_range[0]:
            return self.vision_minimal
        return ''

    def sensed_description(self, lifeform, sense):
        if sense > self.sense_range[1]:
            return self.sense_ideal
        if sense > self.sense_range[0]:
            return self.sense_minimal
        return ''

    def set_sensory_results(self, minimal, ideal, sense_range):
        self.sense_range = sense_range
        self.sense_minimal = minimal
        self.sense_ideal = ideal

    def set_vision_results(self, minimal, ideal, vision_range):
        self.vision_range = vision_range
        self.vision_minimal = minimal
        self.vision_ideal = ideal

    def on_inspect(self, lifeform):
        acu, sen = [lifeform.calculate_effective_stat(x) for x in ['acuity', 'sense']]
        visual = self.visual_description(lifeform, acu)
        sensory = self.sensed_description(lifeform, sen)
        if visual is not '' and sensory is not '':
            return '{} {}'.format(visual, sensory)
        return visual if visual is not '' else sensory

    def necessary_sense(self):
        return 0

    def necessary_acuity(self):
        return 0

