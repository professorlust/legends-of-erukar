from ..ActionCommand import ActionCommand
from erukar.system.engine import ActivatedAbility


class ActivateAbility(ActionCommand):
    def perform(self):
        ability = self.get_ability()
        if not ability:
            return self.fail('Ability not found')
        return ability.perform(self)

    def get_ability(self):
        player = self.args['player_lifeform']
        for ability in player.skills:
            if not isinstance(ability, ActivatedAbility):
                continue
            if ability.__module__ == self.args['abilityModule']:
                return ability
