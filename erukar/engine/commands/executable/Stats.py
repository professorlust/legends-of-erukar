from erukar.engine.model import Command
from erukar.engine.lifeforms import Lifeform

class Stats(Command):
    status = 'STATUS\n----------\nHealth:    {} / {}\nEff. AC:   {}\n'
    attributes = 'ATTRIBUTES\n----------\n{}'
    stat = "{0:10} {1}"

    def execute(self, *_):
        player = self.find_player()
        lifeform = self.lifeform(player)

        status = self.status.format(lifeform.health, lifeform.max_health, lifeform.calculate_armor_class())
        atts = '\n'.join([Stats.stat.format(stat.capitalize(), player.character.get(stat)) \
            for stat in Lifeform.attribute_types])

        return status + self.attributes.format(atts) + '\n'
