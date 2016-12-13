from erukar.engine.model import Modifier
from erukar.engine.lifeforms import Enemy

class EnemyModifier(Modifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Enemy]
    DeprecatesModifiers = []

    def apply_to(self, enemy):
        enemy.modifiers = list(self.deprecate_existing_modifiers(enemy.modifiers))
        enemy.modifiers.append(self)

    def deprecate_existing_modifiers(self, modifiers):
        for mod in modifiers:
            if not any(x for x in self.DeprecatesModifiers if issubclass(type(mod), x)):
                yield mod
