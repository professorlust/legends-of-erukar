from .Lifeform import Lifeform
from erukar.ext.math.Distance import Distance
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
        radius = int(w/3)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2), int(w/2))))
        inner = list(Distance.points_in_circle(int(w/4)-1, (int(h/2),int(w/2))))
        center = list(Distance.points_in_circle(int(w/6)-1, (int(h/2),int(w/2))))

        for y in range(h):
            for x in range(w):
                yield Npc.get_pixel((x, y), circle, inner, center)

    def get_pixel(point, circle, inner, center):
        if point in center:
            return {'r': 240, 'g': 220, 'b': 0, 'a': 1}
        if point in inner:
            return {'r': 240, 'g': 190, 'b': 0, 'a': 1}
        if point in circle:
            return {'r': 0, 'g': 0, 'b': 0, 'a': 1}
        return {'r': 0, 'g': 0, 'b': 0, 'a': 0}

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
