from erukar.engine.commands.Command import Command
import erukar

class LocalIndex(Command):
    NeedsArgs = False

    def perform(self):
        coords = self.args['player_lifeform'].coordinates
        room = self.world.get_room_at(coords)
        contents = [LocalIndex.format_item(x) for x in self.all_targets() if x is not self.args['player_lifeform'] and hasattr(x, 'uuid')]
        self.append_result(self.player_info.uid, contents)
        return self.succeed()

    def all_targets(self):
        return self.world.actors_in_range(self.args['player_lifeform'].coordinates, 3)

    def format_item(item):
        results = {
            'uuid': str(item.uuid), 
            'name': item.alias(),
            'actions': ['Inspect', 'Glance']
        }
        if isinstance(item, erukar.engine.inventory.Item):
            results['actions'].append('Take')
        if isinstance(item, erukar.engine.lifeforms.Enemy):
            results['actions'].append('Attack')
        if isinstance(item, erukar.engine.environment.Container) or isinstance(item, erukar.engine.environment.Door):
            if item.can_open():
                results['actions'].append('Open')
            if item.can_close():
                results['actions'].append('Close')
        return results

    def get_contents(self, room):
        for item in room.contents:
            if item is not self.args['player_lifeform'] and hasattr(item, 'uuid'):
                yield LocalIndex.format_item(item)
