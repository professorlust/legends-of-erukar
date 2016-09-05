from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform

class Stats(Command):
    status = 'STATUS\n----------\nHealth:    {} / {}\nEff. AC:   {}\n\n'
    attributes = 'ATTRIBUTES\n----------\n{}'
    stat = "{0:10} {1}"

    def execute(self, *_):
        player = self.find_player()
        lifeform = self.lifeform(player)

        status_description = self.status.format(
            lifeform.health, 
            lifeform.max_health, 
            lifeform.calculate_armor_class())

        attribute_description = '\n'.join([Stats.stat.format(stat.capitalize(), \
            player.character.calculate_stat_score(stat)) \
            for stat in Lifeform.attribute_types])

        return self.succeed(status_description + self.attributes.format(attribute_description) + '\n')
