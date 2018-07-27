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
        if conversation:
            self.conversation = __import__(conversation).create(self)

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
        scalar = 1 / (x/8 + 1)
        r = 200 + 50 * scalar
        g = 150 + 50 * scalar
        b = 50 * scalar
        return {'r': r, 'g': g, 'b': b, 'a': 1}

    def get_state(self, for_player):
        if self.templates:
            return self.templates[0].get_state(for_player)
        return {}

    def template(self, template_type):
        return next((x for x in self.templates if isinstance(x, template_type)), None)

    def use_standard_inventory(self):
        for template in self.templates:
            self.inventory += template.standard_inventory()

    def disposition_for(self, target):
        bonus = target.disposition_bonuses(self) if isinstance(target, Lifeform) else 0
        if target in self.disposition_modifiers:
            bonus += self.disposition_modifiers[target]
        return bonus

    def player_stop(self, player):
        if self.conversation:
            self.conversation.exit(player.lifeform())
