from .ActivatedAbility import ActivatedAbility


class TargetedAbility(ActivatedAbility):
    def valid_at(self, cmd, loc):
        return True

    def action_for_map(self, cmd, loc):
        yield {
            'name': self.Name,
            'command': 'ActivateAbility',
            'description': self.Name,
            'cost': self.ap_cost(cmd, loc),
            'abilityModule': self.__module__,
        }

    def ap_cost(self, cmd, loc):
        return 1
