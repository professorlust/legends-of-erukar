from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
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
            self.append_missed_attack_results(attack_roll)
            return

        if weapon is None:
            weapon = erukar.engine.inventory.UnarmedStrike()

        result = self.target.apply_damage(weapon.damages, self.character, efficacy)
        self.append_successful_attack_results(attack_roll, weapon, result)

    def append_missed_attack_results(self, attack_roll):
        self.append_if_uid(self.target, '{} missed an attack against you!'.format(self.character.alias()))
        self.append_result(self.sender_uid, 'Your attack ({}) missed {}!'.format(attack_roll, self.target.alias()))

    def append_successful_attack_results(self, attack_roll, weapon, damage_result):
        if damage_result.stopped_by_deflection:
            self.append_deflection_results(attack_roll, weapon, damage_result)
            return

        if damage_result.stopped_by_mitigation:
            self.append_mitigation_results(attack_roll, weapon, damage_result)
            return

        if damage_result.caused_death:
            self.append_death_results(weapon, damage_result)
            return
        
        self.append_damage_results(attack_roll, weapon, damage_result)

    def append_deflection_results(self, attack_roll, weapon, damage_result):
        damage_string = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports])
        self.append_if_uid(self.target, '{}\'s attack with {} hits you, but you deflect all {}!'.format(self.character.alias(), weapon.alias(), damage_string))
        self.append_result(self.sender_uid, 'Your attack ({}) with {} hits {}, but all {} was deflected!'.format(attack_roll, weapon.alias(), self.target.alias(), damage_string))

    def append_mitigation_results(self, attack_roll, weapon, damage_result):
        attacker_results = []
        target_results = []

        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])

        target_results.append('{}\'s attack with {} hits you!'.format(self.character.alias(), weapon.alias()))
        attacker_results.append('Your attack ({}) with {} hits {}!'.format(attack_roll, weapon.alias(), self.target.alias()))

        if len(deflection) > 0:
            target_results.append('Your armor deflected {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflected {} damage.'.format(self.target.alias(), deflection))

        target_results.append('Your armor mitigated {} damage, preventing you from taking any damage!'.format(mitigation))
        attacker_results.append('{}\'s armor mitigated the remaining {} damage.'.format(self.target.alias(), mitigation))
        
        self.append_if_uid(self.target, '\n'.join(target_results))
        self.append_result(self.sender_uid, '\n'.join(attacker_results))

    def append_damage_results(self, attack_roll, weapon, damage_result):
        attacker_results = []
        target_results = []
        deflection = ', '.join(['{} {}'.format(x.amount_deflected, x.damage_type) for x in damage_result.reports if x.amount_deflected > 0])
        mitigation = ', '.join(['{} {}'.format(x.amount_mitigated, x.damage_type) for x in damage_result.reports if x.amount_mitigated > 0])
        actual_damage = ', '.join(['{} {}'.format(x.amount_dealt, x.damage_type) for x in damage_result.reports if x.amount_dealt > 0])

        target_results.append('{}\'s attack with {} hits you!'.format(self.character.alias(), weapon.alias()))
        attacker_results.append('Your attack ({}) with {} hits {}!'.format(attack_roll, weapon.alias(), self.target.alias()))

        if len(deflection) > 0:
            target_results.append('Your armor deflected {} damage!'.format(deflection))
            attacker_results.append('{}\'s armor deflected {} damage.'.format(self.target.alias(), deflection))

        if len(mitigation) > 0:
            target_results.append('Your armor mitigated {} damage!!'.format(mitigation))
            attacker_results.append('{}\'s armor mitigated {} damage.'.format(self.target.alias(), mitigation))

        target_results.append('You take {} damage!'.format(actual_damage))
        attacker_results.append('{} takes {} damage!'.format(self.target.alias(), actual_damage))

        if damage_result.caused_incapacitated:
           target_results.append('You have been incapacitated by {}\'s {}!'.format(self.character.alias(), weapon.alias()))
           attacker_results.append('You have incapacitated {}!'.format(self.target.alias()))

        self.append_if_uid(self.target, '\n'.join(target_results))
        self.append_result(self.sender_uid, '\n'.join(attacker_results))

    def append_death_results(self, weapon, damage_result):
        attacker_results = []
        target_results = []
        target_results.append('You have been slain by {}...'.format(self.character.alias()))
        attacker_results.append('You have slain {}!'.format(self.target.alias()))

        self.append_if_uid(self.target, '\n'.join(target_results))
        self.append_result(self.sender_uid, '\n'.join(attacker_results))
