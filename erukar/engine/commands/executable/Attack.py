from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
import erukar, random, math

class Attack(ActionCommand):
    not_found = "No object matching '{}' was found in this room."
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    UnableToAttackInDirection = "You are unable to perform a directional attack."
    UnableToAttackInRoom = "You are unable to perform an attack."
    MultipleOptions = "Multiple matches for '{}' were found, please specify with a number between 1 and {}.\n\n{}"

    aliases = ['attack']

    def execute(self):
        self.character = self.find_player().lifeform()
        payload = self.check_for_arguments()

        # The payload is a reference; infer that it's in the room and we can attack it
        if isinstance(payload, erukar.engine.model.Describable):
            target = payload
        else:
            # Determine if this is directional attack
            direction = self.determine_direction(payload.lower())
            if direction is not None:
                return self.do_directional_attacks(direction)

            # Get the number of items matching the payload
            targets = self.find_in_room(self.character.current_room, payload)
            if len(targets) == 0:
                return self.fail(self.not_found.format(payload))

            # If there's more than one, we must ask for clarification
            if len(targets) > 1:
                target_list = self.enumerate_options(targets)
                return self.fail(self.MultipleOptions.format(payload, len(targets), target_list))

            # otherwise there is exactly one and that's what we want
            target = targets[0]

        if target is None:
            return self.fail(Attack.not_found.format(payload))
        return self.do_attack(target)

    def enumerate_options(self, targets):
        return '\n'.join(['{:3}. {}'.format(i+1, x.alias()) for i,x in enumerate(targets)])

    def check_for_arguments(self):
        '''
        Check to see if it's a single attack made with either hand, or if
        it's both hands. In the event of a single attack, that attack only
        incurs handedness penalty (left hand attacks with right hand dominant
        take a slight penalty based on dexterity and vice versa), whereas
        attacking with both weapons incurs a larger penalty for each attack.
        The lifeform will eventually need to make a decision for itself as
        to what hand is dominant.
        '''
        payload = self.payload()
        # If this is an instance, then we want that and only that
        if isinstance(payload, erukar.engine.model.Describable):
            return payload

        for r in ['main ', 'primary ', 'right ']:
            if payload[:len(r)] == r:
                self.weapons = [getattr(self.character, 'right')]
                return payload[:len(r)]

        for r in ['off ', 'offhand ', 'left ']:
            if payload[:len(r)] == r:
                self.weapons = [getattr(self.character, 'left')]
                return payload[:len(r)]

        return payload

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

    def do_attack(self, target):
        '''Attack an enemy within the current room'''
        print(target)

        # Attack with each weapon, keeping track of the penalties for dual wielding each time
        dual_wielding_penalty = 1.0
        for attacking_slot in self.character.attack_slots:
            weapon = getattr(self.character, attacking_slot)
            if not self.can_attack_with(weapon): continue
            self.adjudicate_attack(weapon, target, penalty=dual_wielding_penalty)
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
            target = random.choice(targets)
            total_penalty = weapon.RangePenalty * distance * penalty
            return self.adjudicate_attack(weapon, target, total_penalty)

        return self.fail('Your weapon does not have the range to attack {}.'.format(direction.name))

    def adjudicate_attack(self, weapon, enemy, penalty=1.0):
        '''Used to actually resolve an attack roll made between a character and target'''
        attack_roll, evasion, damages = self.calculate_attack(weapon, enemy, penalty)

        args = {
            'subject': self.character.alias(),
            'target': enemy.alias(),
            'weapon_name': 'unarmed attack' if weapon is None else weapon.alias(),
            'roll': attack_roll}

        if attack_roll <= evasion:
            # Show failures to subject and enemy
            self.append_result(self.sender_uid, Attack.unsuccessful.format(**args))
            self.append_result(enemy.uid, Attack.unsuccessful.format(**args))
            return

        self.inflict_damage(enemy, damages, weapon)

    def calculate_attack(self, weapon, target, penalty=1.0):
        '''Involves the calculation of armor_class, attack roll, and damage'''
        attack_roll = int(self.character.roll(self.character.stat_random_range('dexterity')) * penalty)
        evasion = target.calculate_armor_class()

        if weapon is not None and isinstance(weapon, erukar.engine.inventory.Weapon):
            damage = [(int(d[0]*penalty), d[1]) for d in weapon.roll(self.character)]
        elif weapon is None:
            strength = self.character.calculate_effective_stat('strength')
            drange = [0, strength]
            damage_type = Damage('bludgeoning',drange,'strength',(random.uniform,(0,4)))
            damage = [(damage_type.roll(target), 'bludgeoning')]
        else:
            return [0,0,[]]

        return [attack_roll, evasion, damage]

