from erukar.ext.math.Distance import Distance
import uuid


class ErukarObject:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.coordinates = (0, 0)

    def tile_id(self):
        return str(self.uuid)

    def ids_to_generate(self):
        return [self.tile_id()]

    def generate_tile(self, dimensions, tile_id):
        '''Erukar Objects are, by default, Basic Blue Circles'''
        h, w = dimensions
        radius = int(w/3)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2),int(w/2))))
        inner_circle = list(Distance.points_in_circle(int(w/4)-1, (int(h/2),int(w/2))))
        for y in range(h):
            for x in range(w):
                if (x,y) in circle and (x,y) not in inner_circle:
                    yield {'r':0,'g':0,'b':200,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}

    def get_object_by_uuid(self, uuid):
        if uuid == self.uuid: 
            return self

    def is_detected(self, acuity, sense):
        return acuity > self.minimum_acuity_to_detect() or sense > self.minimum_sense_to_detect()

    def minimum_sense_to_detect(self):
        return 1

    def minimum_acuity_to_detect(self):
        return 1

    def on_inspect(self, sender):
        pass

    def on_start(self, *_):
        pass

    def on_attack(self, sender):
        pass

    def on_equip(self, sender):
        pass

    def on_move(self, sender):
        pass

    def on_take(self, sender):
        pass

    def on_open(self, sender):
        pass

    def on_close(self, sender):
        pass

    def on_use(self, sender):
        pass

    def on_give(self, sender):
        pass

    def matches(self, other):
        return False

    def get_name(self):
        pass

    def hear(self):
        pass

    def take_damage(self, damage, instigator=None):
        pass

    def on_hear(self, sound, decay=1.0, instigator=None, direction=None):
        pass
