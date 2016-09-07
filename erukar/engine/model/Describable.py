from .Interactible import Interactible
import re

class Describable(Interactible):
    '''Mechanically, the brain can combine two sources of minimal information
    into a full story. Here, we do the same thing with sensory feedback and
    visual feedback. There are three major results with two categories each.
    These include vision, sensory, and detailed; the subsets are a minimal and an
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
        self.detailed_minimal = 'Minimal Visual and Sensory Result'
        self.detailed_ideal = 'Ideal Visual and Sensory Result'''

    def mutate(self, mutatable_string, optional_parameters=None):
        mutation_arguments = {}
        if optional_parameters is not None:
            mutation_arguments = optional_parameters
        # Perform Regex
        captured = re.findall('{(\w*)(?:\|(\w*))*}', mutatable_string)
        # iterate through all of our capture groups 
        for cap in captured:
            target = self
            format_name = cap[0]
            # in the event of a specified target e.g. {prop|target}
            if cap[1] is not None and hasattr(self, cap[1]):
                target = getattr(self, cap[1])
                format_name = '|'.join(cap)
            # Get the value from the target
            if hasattr(target, cap[0]):
                value = getattr(target, cap[0]) 
                if callable(value):
                    value = value()
                mutation_arguments[format_name] = value
        try:
            result = mutatable_string.format(**mutation_arguments)
        except:
            result = mutatable_string
        return result

    def describe_visual(self, lifeform, acuity):
        if acuity >= self.vision_range[1]:
            return self.vision_ideal
        if acuity >= self.vision_range[0]:
            return self.vision_minimal
        return ''

    def describe_sensory(self, lifeform, sense):
        if sense >= self.sense_range[1]:
            return self.sense_ideal
        if sense >= self.sense_range[0]:
            return self.sense_minimal
        return ''

    def describe_detailed(self, lifeform, acuity, sense):
        if acuity >= self.vision_range[1] and sense >= self.sense_range[1]:
            return self.detailed_ideal
        return self.detailed_minimal

    def set_sensory_results(self, minimal, ideal, sense_range):
        self.sense_range = sense_range
        self.sense_minimal = minimal
        self.sense_ideal = ideal

    def set_vision_results(self, minimal, ideal, vision_range):
        self.vision_range = vision_range
        self.vision_minimal = minimal
        self.vision_ideal = ideal

    def set_detailed_results(self, minimal, ideal):
        self.detailed_minimal = minimal
        self.detailed_ideal = ideal

    def describe_base(self, lifeform, acuity, sense):
        '''This should be the entry point for finding things in a room'''
        if acuity >= self.vision_range[0] and sense >= self.sense_range[0]:
            return self.mutate(self.describe_detailed(lifeform, acuity, sense))
        if acuity >= self.vision_range[0]:
            return self.mutate(self.describe_visual(lifeform, acuity))
        if sense >= self.sense_range[0]:
            return self.mutate(self.describe_sensory(lifeform, sense))
        return ''

    def on_inspect(self, lifeform, acuity, sense):
        return self.describe_base(lifeform, acuity, sense)

    def necessary_sense(self):
        return 0

    def necessary_acuity(self):
        return 0

