from erukar.game.modifiers.base.EnemyModifier import EnemyModifier

class EpicQuestTarget(EnemyModifier):
    def apply_to(self, enemy):
        enemy.modifiers = [x for x in enemy.modifiers 
                           if not issubclass(type(x), erukar.game.modifiers.enemy.static.QuestTarget)]
        enemy.modifiers.append(self)
