from .Interactible import Interactible

class Describable(Interactible):
    '''Mechanically, the brain can combine two sources of minimal information
    into a full story. Here, we do the same thing with sensory feedback and
    visual feedback. There are three major results with two categories each.
    These include vision, sensory, and both; the subsets are a minimal and an
    ideal result. The three major categories detail whether only vision or
    sensory minimum was met or at least the minimum for each was met.

    Ideally, this will lead to situations where items appear as purely visual
    "You see a Ceramic Cuirass", invisible events such as air currents are 
    purely sensory "You feel a warm draft of air circulating through the room",
    and combinations are something much more robust "Piercing the floor is a
    heavy-looking sword forged with some sort of dark metal, the blade of which
    is enveloped in bright orange and yellow flames. The flames, though they
    are bright enough to illuminate the room well enough, give off only scant
    heat."
    
    If both Ideals are met, the user should be given even more information,
    though sometimes this is unnecessary.
    '''

    def __init__(self):
        self.vision_range = (0, 1)
        self.vision_minimal = 'Minimal Visual Result'
        self.vision_ideal = 'Ideal Visual Result'
        self.sense_range = (0, 1)
        self.sense_minimal = 'Minimal Sensory Result'
        self.sense_ideal = 'Ideal Sensory Result'
        self.both_minimal = 'Minimal Visual and Sensory Result'
        self.both_ideal = 'Ideal Visual and Sensory Result'''

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

