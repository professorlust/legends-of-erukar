from .Lifeform import Lifeform
from erukar.ext.math.Distance import Distance
from erukar.ext.math.Navigator import Navigator
from erukar.ext.math.Namer import Namer


class Npc(Lifeform):
    def __init__(self, templates=[], conversation=None):
        super().__init__(None, "Npc")
        self.faction = 'iurian'
        self.qualities = []
        self.templates = []
        self.name = Namer.random()
        self.inactive_templates = templates
        self.disposition_modifiers = {}
        self.conversation = __import__(conversation).create(self)\
            if conversation\
            else None

    def generate_tile(self, dimensions, tile_id):
        h, w = dimensions
        center = (int(h/2), int(w/2))
        radius = int(w/3)-1
        border = list(Distance.points_in_circle(radius, center))
        circle = list(Distance.points_in_circle(int(w/4)-1, center))

        for y in range(h):
            for x in range(w):
                yield Npc.get_pixel((x, y), center, circle, border)

    def get_pixel(point, center, circle, border):
        if point not in border:
            return {'r': 0, 'g': 0, 'b': 0, 'a': 0}
        if point in circle:
            return Npc.gradient(point, center)
        return {'r': 0, 'g': 0, 'b': 0, 'a': 1}

    def gradient(point, center):
        x = Navigator.distance(point, center)
        scalar = 1 / (x/4 + 1)
        return {
            'r': 160 + int(90 * scalar),
            'g': 130 + int(70 * scalar),
            'b': int(50 * scalar),
            'a': 1
        }

    def get_state(self, for_player):
        if self.templates:
            return self.templates[0].get_state(for_player)
        return {}

    def template(self, _type):
        for template in self.templates:
            if isinstance(template, _type):
                return template

    def use_standard_inventory(self):
        for template in self.templates:
            self.inventory += template.standard_inventory()

    def disposition_for(self, target):
        bonus = self.disposition_bonuses(target)
        if target in self.disposition_modifiers:
            bonus += self.disposition_modifiers[target]
        return bonus

    def disposition_bonuses(self, target):
        if isinstance(target, Lifeform):
            return target.disposition_bonuses(self)
        return 0

    def player_stop(self, player):
        if self.conversation:
            self.conversation.exit(player.lifeform())
