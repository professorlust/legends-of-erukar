from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
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
        
        if isinstance(self.target, erukar.engine.model.Direction):
            return self.do_directional_attacks()
        return self.do_attack()

    def can_attack_with(self, weapon):
        return weapon is None or isinstance(weapon, erukar.engine.inventory.Weapon)

    def do_directional_attacks(self, direction):
        '''Handles attacking with all queued weapons'''
        room = self.character.current_room

        dual_wielding_penalty = 1.0
        for attacking_slot in self.character.attack_slots:
            weapon = getattr(self.character, attacking_slot)
            if not self.can_attack_with(weapon): continue
            self.attack_in_direction(room, weapon, 0, direction)
            dual_wielding_penalty *= self.character.dual_wielding_penalty

        # Succeed if we have results, otherwise fail with the UnableToAttackInDirection
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInDirection)

    def do_attack(self):
        '''Attack an enemy within the current room'''
        # Attack with each weapon, keeping track of the penalties for dual wielding each time
        dual_wielding_penalty = 1.0
        for attacking_slot in self.character.attack_slots:
            weapon = getattr(self.character, attacking_slot)
            if not self.can_attack_with(weapon): continue
            self.perform_attack(weapon, dual_wielding_penalty)
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

    def perform_attack(self, weapon, efficacy=1.0):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_roll = int(self.character.roll(self.character.stat_random_range('dexterity')) * efficacy)
        evasion = self.target.evasion()
        if attack_roll < evasion:
            PhysicalDamageFormatter.append_missed_attack_results(self, attack_roll)
            return

        if weapon is None:
            weapon = erukar.engine.inventory.UnarmedStrike()

        self.dirty(self.character)
        self.dirty(self.target)
        result = self.target.apply_damage(weapon.damages, self.character, efficacy)
        PhysicalDamageFormatter.process_and_append_damage_result(self, attack_roll, weapon, result)

