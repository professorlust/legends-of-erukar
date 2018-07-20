from erukar.system.engine import TargetedAbility


class Parry(TargetedAbility):
    def validate(self, cmd, player, target, weapon):
        failed = super().validate(self, cmd, player, target, weapon)
        if failed:
            return failed

