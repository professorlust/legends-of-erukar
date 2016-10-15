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
        mutated = self.infer(mutatable_string, optional_parameters)
        post_context = self.contextual_inferrence(mutated, optional_parameters)
        return post_context

    def contextual_inferrence(self, mutatable_string, optional_parameters=None):
        matches = re.finditer('~(\w*)(?:\|(\w*))*~', mutatable_string)
        for match_obj in matches:
            inference_method, target_name = match_obj.groups()
            l_end, r_start = match_obj.span()
            left = mutatable_string[:l_end]
            right = mutatable_string[r_start:]
            target = self

            # in the event of a specified target e.g. {prop|target}
            if target_name is not None and hasattr(self, target_name):
                target = getattr(self, target_name)
                format_name = '|'.join(capture)

            if hasattr(target, inference_method):
                actual_method = getattr(target, inference_method)
                mutatable_string = ''.join([left, actual_method(left, right), right])
        return mutatable_string


    def infer(self, mutatable_string, optional_parameters):
        mutation_arguments = {}
        if optional_parameters is not None:
            mutation_arguments = optional_parameters
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
        except Exception as e:
            result = mutatable_string
        return result

    def a_or_an(self, left, right):
        right = right.lstrip().lower()
        vowel_sound =  (len(right) >= 1 and right[0] in ['a','e','i','o','u','y']) or (len(right) >= 2 and right[:1] in ['ho'] )
        return 'an' if vowel_sound else 'a'

    def on_inspect(self, lifeform, acuity, sense):
        return self.mutate(Describable.get_best_match(self.Inspects, acuity, sense))

    def on_glance(self, lifeform, acuity, sense):
        return self.mutate(Describable.get_best_match(self.Glances, acuity, sense))

    @staticmethod
    def get_best_match(collection, acuity, sense):
        sorted_collection = sorted(collection, key=lambda obs: obs.score(), reverse=True)
        scores = [gl.result for gl in sorted_collection if gl.met(acuity, sense)]
        return '' if len(scores)==0 else scores[0]

