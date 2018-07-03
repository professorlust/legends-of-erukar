from erukar.system.engine import Wait, Attack, Move, Inspect, ActivateAbility
from erukar.system.engine import Player, AiModule


class BasicAI(AiModule):
    def perform_turn(self):
        target, weapons = self.check_for_enemies_in_range()
        if target:
            weapon = self.puppet.right
            if not weapon:
                return self.wait()
            return self.create_attack(target, weapon)

        location = self.check_for_enemies_to_move_to()
        if location:
            return self.move(location)

        return self.wait()

    def check_for_enemies_in_range(self):
        for loc, enemy in self.enemies_in_fow():
            if loc not in self.puppet.zones.weapon_ranges:
                continue
            return enemy, self.puppet.zones.weapon_ranges[loc]
        return None, []

    def check_for_enemies_to_move_to(self):
        for loc, enemy in self.enemies_in_fow():
            return self.get_nearest_coordinate_in_attack_range(loc)
        return None

    def enemies_in_fow(self):
        for loc in self.puppet.zones.fog_of_war:
            for player in self.world.actors_of_type_at(self.puppet, loc, Player):
                if self.puppet.can_detect(player):
                    yield loc, player

    def wait(self):
        return self.create_command(Wait)

    def idle(self):
        return self.create_command(Inspect)

    def create_attack(self, target, weapon):
        cmd = self.create_command(ActivateAbility)
        cmd.args['abilityModule'] = Attack.__module__
        cmd.args['interaction_target'] = target.uuid
        cmd.args['weapon'] = weapon.uuid
        return cmd

    def move(self, location):
        cmd = self.create_command(ActivateAbility)
        cmd.args['abilityModule'] = Move.__module__
        cmd.args['coordinates'] = location
        return cmd

    def get_nearest_coordinate_in_attack_range(self, goal):
        '''Will make more efficient later'''
        path = self.get_path_to(goal)
        max_weapon_range = int(self.puppet.max_weapon_range())
        return path[-int(max_weapon_range + 1)]
