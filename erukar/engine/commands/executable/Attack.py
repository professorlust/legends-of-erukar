from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Damage import Damage
import erukar, random, math

class Attack(ActionCommand):
    not_found = "No object matching '{}' was found in this room."
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    successful = "{subject}'s attack of {roll} hits {target}, dealing {damage} damage."
    caused_dying = "\n{target} has been incapacitated by {subject}'s attack!"
    caused_death = "\n{target} has been slain by {subject}!"
    deflected = '{target}\'s armor deflected the entirety of the damage from {subject}!'
    UnableToAttackInDirection = "You are unable to perform a directional attack."
    UnableToAttackInRoom = "You are unable to perform an attack."
    EnemyFullMitigation = "{target}'s armor absorbed the entirety of your {weapon_name}'s damage!"
    YourFullMitigation = "Your armor absorbed the entirety of the damage from {target}'s {weapon_name}!"

    aliases = ['attack']

    def execute(self):
        self.character = self.find_player().lifeform()
        payload = self.check_for_arguments()

        # Determine if this is directional attack
        direction = self.determine_direction(payload.lower())
        if direction is not None:
            return self.do_directional_attacks(direction)

        return self.do_attack(payload)

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
        for attacking_slot in self.character.attack_slots:
            weapon = getattr(self.character, attacking_slot)
            if not self.can_attack_with(weapon): continue
            self.attack_in_direction(room, weapon, 0, direction)
        # Succeed if we have results, otherwise fail with the UnableToAttackInDirection
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInDirection)

    def do_attack(self, payload):
        '''Attack an enemy within the current room'''
        target = self.find_in_room(self.character.current_room, payload)
        if target is None:
            return self.fail(Attack.not_found.format(payload))
        for attacking_slot in self.character.attack_slots:
            weapon = getattr(self.character, attacking_slot)
            if not self.can_attack_with(weapon): continue
            self.adjudicate_attack(weapon, target)
        # Succeed if we have results, otherwise fail with the UnableToAttackInRoom
        return self.succeed_if_any_results(msg_if_failure=self.UnableToAttackInRoom)

    def attack_in_direction(self, room, weapon, distance, direction):
        ''' Attack in direction; logic for what gets hit (door, room, or wall) goes here'''
        adj_room = room.get_in_direction(direction)

        # Are we going to hit a door?
        if adj_room.door is not None \
            and isinstance(adj_room.door, erukar.engine.environment.Door):
            if adj_room.door.status is not Door.Open:
                return self.append_result(self.sender_uid, 'You have attacked a door.')

        # are we actually able to hit the room in this direction (and does it exist?)
        if adj_room.room is not None:
            return self.attack_into_room(adj_room.room, weapon, distance+1, direction)
        return self.append_result(self.sender_uid, 'You attack a wall. Are you happy now?')

    def attack_into_room(self, room, weapon, distance, direction):
        '''Check to see if there's a target in this room to attack; attack if so'''
        if weapon.AttackRange >= distance:
            targets = [c for c in room.contents if isinstance(c, erukar.engine.lifeforms.Lifeform)]
            if len(targets) < 1:
                return self.attack_in_direction(room, weapon, distance, direction)

            # Actually Attack
            target = random.choice(targets)
            penalty = weapon.RangePenalty * distance
            return self.adjudicate_attack(weapon, target, penalty)

        return self.fail('Your weapon does not have the range to attack {}.'.format(direction.name))

    def adjudicate_attack(self, weapon, enemy, roll_penalty=0):
        '''Used to actually resolve an attack roll made between a character and target'''
        raw_attack_roll, armor_class, damages = self.calculate_attack(weapon, enemy)
        attack_roll = raw_attack_roll - roll_penalty

        args = {
            'subject': self.character.alias(),
            'target': enemy.alias(),
            'weapon_name': 'unarmed attack' if weapon is None else weapon.alias(),
            'roll': attack_roll}

        if attack_roll <= armor_class:
            # Show failures to subject and enemy
            self.append_result(self.sender_uid, Attack.unsuccessful.format(**args))
            self.append_result(enemy.uid, Attack.unsuccessful.format(**args))
            return

        # Calculate the actual damage through mitigation and deflection
        actuals = []
        for damage_amount, damage_type in damages:
            if enemy.deflection(damage_type) >= damage_amount:
                self.append_result(self.sender_uid, Attack.deflected.format(**args))
                self.append_result(enemy.uid, Attack.deflected.format(**args))
                continue
            actual_damage = int(enemy.mitigation(damage_type) * damage_amount)
            if actual_damage > 0:
               actuals.append((actual_damage, damage_type))

        # Calculate the Damage  
        damage = sum(amt for amt, _ in actuals)
        if damage <= 0:
            self.append_result(self.sender_uid, Attack.EnemyFullMitigation.format(**args))
            self.append_result(enemy.uid, Attack.YourFullMitigation.format(**args))
            return

        # Apply the damage
        self.dirty(enemy)
        args['damage'] = ', '.join(["{} {}".format(*x) for x in actuals if x[0] > 0])
        xp = enemy.take_damage(damage, self.character)
        attack_string = Attack.successful.format(**args)

        # Check to see if Dying, or Dead.
        if hasattr(enemy, 'afflictions'):
            if enemy.afflicted_with(erukar.engine.effects.Dying):
                attack_string = attack_string + Attack.caused_dying.format(**args)

            if enemy.afflicted_with(erukar.engine.effects.Dead):
                self.create_corpse(enemy)
                attack_string = attack_string + Attack.caused_death.format(**args)

        # Let everyone know what happened
        self.append_result(self.sender_uid, attack_string)
        self.append_result(enemy.uid, attack_string)

        if xp <= 0: return
        xp_awards = self.character.award_xp(xp)
        for award in xp_awards:
            self.append_result(self.sender_uid, award)


    def create_corpse(self, target):
        room = target.current_room
        if target in room.contents:
            room.contents.remove(target)
        room.add(Corpse(target))

    def calculate_attack(self, weapon, target):
        '''Involves the calculation of armor_class, attack roll, and damage'''
        attack_roll = self.character.roll(self.character.stat_random_range('dexterity'))
        armor_class = target.calculate_armor_class()
        if weapon is not None and isinstance(weapon, erukar.engine.inventory.Weapon):
            damage = weapon.roll(self.character)
        elif weapon is None:
            strength = self.character.calculate_effective_stat('strength')
            drange = [0, strength]
            damage_type = Damage('bludgeoning',drange,'strength',(random.uniform,(0,4)))
            damage = [(damage_type.roll(target), 'bludgeoning')]
        else:
            return [0,0,[]]

        return [attack_roll, armor_class, damage]

