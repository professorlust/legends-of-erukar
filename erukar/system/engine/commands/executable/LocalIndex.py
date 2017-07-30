from erukar.system.engine import Weapon, Container, Door, Enemy, Item
from ..Command import Command

class LocalIndex(Command):
    NeedsArgs = False

    def perform(self):
        coords = self.args['player_lifeform'].coordinates
        contents = [self.format_item(x) for x in self.all_targets() if x is not self.args['player_lifeform'] and hasattr(x, 'uuid')]
        self.append_result(self.player_info.uid, contents)
        return self.succeed()

    def all_targets(self):
        for loc in self.args['player_lifeform'].zones.fog_of_war:
            yield from self.world.actors_at(self.args['player_lifeform'], loc)

    def format_item(self, item):
        results = {
            'uuid': str(item.uuid), 
            'name': item.alias(),
            'actions': [LocalIndex.format_action('Inspect'), LocalIndex.format_action('Glance')]
        }
        if isinstance(item, Item):
            results['actions'].append(LocalIndex.format_action('Take'))

        if isinstance(item, Enemy):
            for item in [self.args['player_lifeform'].left, self.args['player_lifeform'].right]:
                if issubclass(type(item), Weapon):
                    results['actions'].append({
                        'name': 'Attack with {}'.format(item.alias()),
                        'command': 'Attack',
                        'weapon': str(item.uuid)
                    })

        if isinstance(item, Container) or isinstance(item, Door):
            if item.can_open():
                results['actions'].append(LocalIndex.format_action('Open'))
            if item.can_close():
                results['actions'].append(LocalIndex.format_action('Close'))
        return results

    def get_contents(self, room):
        for item in room.contents:
            if item is not self.args['player_lifeform'] and hasattr(item, 'uuid'):
                yield LocalIndex.format_item(item)

    def format_action(title, command=''):
        if not command: command = title
        return {
            'command': command,
            'name': title
        }
