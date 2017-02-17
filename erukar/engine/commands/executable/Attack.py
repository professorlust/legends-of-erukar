from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
from erukar.engine.model.AttackState import AttackState
from erukar.engine.formatters.PhysicalDamageFormatter import PhysicalDamageFormatter
from erukar.engine.calculators.Navigator import Navigator
import erukar, random, math

class Attack(ActionCommand):
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    UnableToAttackInDirection = "You are unable to perform a directional attack."
    UnableToAttackInRoom = "You are unable to perform an attack."

    aliases = ['attack']
    TrackedParameters = ['target']

    def execute(self):
        self.character = self.find_player().lifeform()
        self.room = self.character.current_room

        failure = self.check_for_arguments()
        if failure: return failure

        return self.do_attack()

    def build_attack_state(self):
        '''Factory method'''
        attack_state = AttackState()
        attack_state.attacker = self.character
        attack_state.target = self.target
        return attack_state

    def do_attack(self):
        '''Attack an enemy within the current room'''
        # Attack with each weapon, keeping track of the penalties for dual wielding each time
        direction = self.target if isinstance(self.target, erukar.engine.model.Direction) else None
        dual_wielding_penalty = 1.0

        for attacking_slot in self.character.attack_slots:
            new_attack = self.build_attack_state()
            new_attack.efficiency = dual_wielding_penalty
            new_attack.get_weapon(attacking_slot, use_unarmed_if_none=True)
            if isinstance(new_attack.weapon, erukar.engine.inventory.Weapon) and new_attack.weapon.RequiresAmmo:
                new_attack.ammunition = self.character.ammunition
            new_attack.attack_direction = direction
            if not new_attack.is_valid():
                continue
            self.perform_attack(new_attack)
            dual_wielding_penalty *= self.character.dual_wielding_penalty

        # Succeed if we have results, otherwise fail with the UnableToAttackInRoom
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInRoom)

    def perform_attack(self, attack_state):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_state.calculate_attack()

        if not attack_state.attack_successful():
            PhysicalDamageFormatter.append_missed_attack_results(self, attack_state)
            return

        self.dirty(self.character)
        self.dirty(self.target)

        attack_state.on_process_damage(self)
        attack_state.confirm()
        PhysicalDamageFormatter.process_and_append_damage_result(self, attack_state)

        if attack_state.processed_damage_result.xp_value > 0:
            self.character.award_xp(attack_state.processed_damage_result.xp_value, self)

    def resolve_directional_target(self, direction):
        '''Find all visible targets in a line extending to the {direction}'''
        acuity, sense = self.character.get_detection_pair()
        targets = {}
        room = self.character.current_room
        passage = room.get_in_direction(direction)

        while passage.can_see_through() and (acuity > 0 or sense > 0):
            acuity -= 10
            sense -= 10
            room = passage.room

            for target in room.detected_lifeforms(self.character, acuity, sense):
                distance = Navigator.distance(room.coordinates, self.character.current_room.coordinates)
                target_string = '{} ({} feet to the {})'.format(target.alias(), int(distance*5), direction.name)
                targets[target_string] = target
            passage = room.get_in_direction(direction)

        return self.find_in_dictionary('', targets, 'target')

