import random, string

class TransitionState:
    def __init__(self):
        self.identifier = ''
        self.coordinates = (0,0)
        self.is_random = False
        self.generation_properties = None
        self.previous_identifier = ''

    def random(generation_properties):
        f = TransitionState()
        f.is_random = True
        chars = string.ascii_uppercase + string.digits
        f.identifier = ''.join(random.choice(chars) for x in range(64))
        f.generation_properties = generation_properties
        return f

    def hub(identifier, coordinates):
        f = TransitionState()
        f.identifier = identifier
        f.coordinates = coordinates
        return f
