from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
from erukar.engine.model.AttackState import AttackState
from erukar.engine.formatters.PhysicalDamageFormatter import PhysicalDamageFormatter
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
            new_attack.attack_direction = direction
            if not new_attack.is_valid():
                continue
            self.perform_attack(new_attack)
            dual_wielding_penalty *= self.character.dual_wielding_penalty

        # Succeed if we have results, otherwise fail with the UnableToAttackInRoom
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInRoom)

    def attack_in_direction(self, room, weapon, distance, direction, penalty=1.0):
        ''' Attack in direction; logic for what gets hit (door, room, or wall) goes here'''
        adj_room = room.get_in_direction(direction)

        # Are we going to hit a door?
        if adj_room.door is not None \
            and isinstance(adj_room.door, erukar.engine.environment.Door):
            if adj_room.door.status is not Door.Open:
                return self.append_result(self.sender_uid, 'You have attacked a door.')

        # are we actually able to hit the room in this direction (and does it exist?)
        if adj_room.room is not None:
            return self.attack_into_room(adj_room.room, weapon, distance+1, direction, penalty)
        return self.append_result(self.sender_uid, 'You attack a wall. Are you happy now?')

    def attack_into_room(self, room, weapon, distance, direction, penalty=1.0):
        '''Check to see if there's a target in this room to attack; attack if so'''
        if weapon.AttackRange >= distance:
            targets = [c for c in room.contents if isinstance(c, erukar.engine.lifeforms.Lifeform)]
            if len(targets) < 1:
                return self.attack_in_direction(room, weapon, distance, direction)

            # Actually Attack
            self.target = random.choice(targets)
            total_penalty = weapon.RangePenalty * distance * penalty
            self.perform_attack(weapon, total_penalty)

        return self.fail('Your weapon does not have the range to attack {}.'.format(direction.name))

    def perform_attack(self, attack_state):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_state.calculate_attack()

        if not attack_state.attack_successful():
            PhysicalDamageFormatter.append_missed_attack_results(self, attack_state)
            return

        self.dirty(self.character)
        self.dirty(self.target)

        attack_state.on_apply_damage()
        PhysicalDamageFormatter.process_and_append_damage_result(self, attack_state)
