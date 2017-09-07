from erukar.system.engine import ErukarActor

class TransitionPiece(ErukarActor):
    def __init__(self, origin, destination):
        super().__init__()
        self.origin = origin
        self.destination = destination

    def generate_tile(self, dimensions):
        h, w = dimensions
        for y in range(h):
            for x in range(w):
                if 3 < y < (h-3) and 3 < x < (w-3):
                    yield {'r': 180, 'g': 180, 'b':0, 'a': 1}
                else: yield {'r':0,'g':0,'b':0,'a':0}
