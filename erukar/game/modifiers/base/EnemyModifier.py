from erukar.engine.model import Modifier
from erukar.engine.lifeforms import Enemy

class EnemyModifier(Modifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Enemy]

    def apply_to(self, enemy):
        enemy.modifiers.append(self)

