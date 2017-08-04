from erukar.system.engine import Lifeform
from ..Command import Command

class Skills(Command):
    NeedsArgs = False

    def perform(self):
        available = []
        acquired = [{
            'name': skill.Name,
            'level': skill.level,
            'nextLevel': skill.next_level_description(),
            'maxLevel': 8,
            'description': skill.current_level_description()}
            for skill in self.args['player_lifeform'].skills
        ]
        full_list = {
            'available': available,
            'acquired': acquired
        }
        self.append_result(self.player_info.uid, full_list)
        return self.succeed()
