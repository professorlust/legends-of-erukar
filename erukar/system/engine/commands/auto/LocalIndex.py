from erukar.system.engine import Weapon, Container, Door, Enemy, Item
from ..Command import Command


class LocalIndex(Command):
    NeedsArgs = False

    def perform(self):
        contents = list(self.get_contents())
        self.append_result(self.player_info.uid, contents)
        return self.succeed()

    def get_contents(self):
        lifeform = self.args['player_lifeform']
        for target in self.all_targets():
            if not hasattr(target, 'uuid') or target is lifeform:
                continue
            yield self.format_item(target)

    def all_targets(self):
        for loc in self.args['player_lifeform'].zones.fog_of_war:
            yield from self.world.actors_at(self.args['player_lifeform'], loc)

    def format_item(self, item):
        results = {
            'uuid': str(item.uuid),
            'name': item.alias(),
            'actions': [
                LocalIndex.format_action('Inspect'),
                LocalIndex.format_action('Glance')
            ]
        }
        if isinstance(item, Item):
            results['actions'].append(LocalIndex.format_action('Take'))

        if isinstance(item, Enemy):
            for weapon in self.valid_attack_weapons():
                results['actions'].append({
                    'name': LocalIndex.format_attack_text(item, weapon),
                    'command': 'Attack',
                    'weapon': str(item.uuid)
                })

        if isinstance(item, Container) or isinstance(item, Door):
            if item.can_open():
                results['actions'].append(LocalIndex.format_action('Open'))
            if item.can_close():
                results['actions'].append(LocalIndex.format_action('Close'))
        return results

    def format_attack_text(enemy, weapon):
        return 'Attack {} with {}'.format(enemy.alias(), weapon.alias())

    def valid_attack_weapons(self):
        lifeform = self.args['player_lifeform']
        for item in [lifeform.left, lifeform.right]:
            if issubclass(type(item), Weapon):
                yield item

    def format_action(title, command=''):
        if not command:
            command = title
        return {
            'command': command,
            'name': title
        }
