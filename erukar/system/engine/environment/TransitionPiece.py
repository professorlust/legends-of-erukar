from erukar.system.engine import ErukarActor
import math

class TransitionPiece(ErukarActor):
    def __init__(self, origin, destination):
        super().__init__()
        self.origin = origin
        self.destination = destination

    def generate_tile(self, dimensions, tile_id):
        h, w = dimensions
        for y in range(h):
            for x in range(w):
                y_i = math.floor(x/2)
                if y_i < y < (h-y_i) and 3 < x < (w-3):
                    yield {'r': 180, 'g': 180, 'b':0, 'a': 1}
                else: yield {'r':0,'g':0,'b':0,'a':0}

    def alias(self, *_):
        return 'TRANSITIONING PIECE'
