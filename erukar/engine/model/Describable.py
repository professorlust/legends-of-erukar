from erukar.engine.model.Observation import Observation
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
    Glances = []
    Inspects = []

    MaximumMutationDepth = 4

    def set_vision_results(self, minimal, ideal, vision_range, *_):
        pass

    def set_sensory_results(self, minimal, ideal, sense_range, *_):
        pass

    def set_detailed_results(self, *_):
        pass

    def erjoin(list_to_join):
        '''English readable Join. Adds commas and an "and".'''
        comma = ', '
        if any(',' in x for x in list_to_join):
            comma = '; ' # Hypercomma
        list_to_join = [x for x in list_to_join if x is not '']
        if len(list_to_join) > 1:
            list_to_join[-1] = 'and ' + list_to_join[-1]
        if len(list_to_join) > 2:
            return comma.join(list_to_join)
        return ' '.join(list_to_join)

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

    def on_inspect(self, lifeform, acuity, sense):
        sorted_inspects = sorted(self.Inspects, key=lambda obs: obs.score(), reverse=True)
        scores = [ins.result for ins in sorted_inspects if ins.met(acuity, sense)]
        return '' if len(scores)==0 else scores[0]

    def on_glance(self, lifeform, acuity, sense):
        sorted_glances = sorted(self.Glances, key=lambda obs: obs.score(), reverse=True)
        scores = [gl.result for gl in sorted_glances if gl.met(acuity, sense)]
        return '' if len(scores)==0 else scores[0]
