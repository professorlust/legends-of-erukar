from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Corpse import Corpse
from erukar.engine.environment.Door import Door
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar, random

class Attack(ActionCommand):
    not_found = "No object matching '{}' was found in this room."
    unsuccessful = "{subject}'s attack of {roll} misses {target}."
    successful = "{subject}'s attack of {roll} hits {target}, dealing {damage} damage."
    caused_dying = "\n{target} has been incapacitated by {subject}'s attack!"
    caused_death = "\n{target} has been slain by {subject}!"

    def execute(self):
        player = self.find_player()
        lifeform = self.lifeform(player)

        self.check_for_arguments(lifeform)

        if len(self.weapons) == 0:
            return self.fail('You must equip a weapon in order to attack')

        # Determine if this is directional attack
        direction = self.determine_direction(self.payload.lower())
        if direction is not None:
            return self.succeed(self.do_directional_attacks(lifeform, direction))

        return self.succeed(self.do_attack(lifeform))

    def check_for_arguments(self, lifeform):
        '''
        Check to see if it's a single attack made with either hand, or if 
        it's both hands. In the event of a single attack, that attack only
        incurs handedness penalty (left hand attacks with right hand dominant
        take a slight penalty based on dexterity and vice versa), whereas 
        attacking with both weapons incurs a larger penalty for each attack.
        The lifeform will eventually need to make a decision for itself as
        to what hand is dominant.
        '''
        for r in ['main ', 'primary ', 'right ']:
            if self.payload[:len(r)] == r:
                self.weapons = [getattr(lifeform, 'right')]
                self.payload = self.payload[:len(r)]
                return

        for r in ['off ', 'offhand ', 'left ']:
            if self.payload[:len(r)] == r:
                self.weapons = [getattr(lifeform, 'left')]
                self.payload = self.payload[:len(r)]
                return

        self.weapons = [getattr(lifeform, hand) for hand in ['left','right'] \
                            if self.can_attack_with_hand(lifeform, hand)]

    def can_attack_with_hand(self, lifeform, hand):
        weapon = getattr(lifeform, hand)
        return weapon is not None \
                and isinstance(weapon, erukar.engine.inventory.Weapon)

    def do_directional_attacks(self, lifeform, direction):
        '''Handles attacking with all queued weapons''' 
        attack_results = []
        room = lifeform.current_room
        for weapon in self.weapons:
            if weapon is None: continue
            res = self.attack_in_direction(lifeform, room, weapon, 0, direction)
            attack_results.append(res)
        return '\n'.join(attack_results)

    def do_attack(self, lifeform):
        '''Attack an enemy within the current room'''
        attack_results = []
        target = self.find_in_room(lifeform.current_room, self.payload)
        if target is None:
            return Attack.not_found.format(self.payload)
        for weapon in self.weapons:
            if weapon is None: continue
            res = self.adjudicate_attack(lifeform, weapon, target)
            attack_results.append(res)
        return '\n'.join(attack_results)

    def attack_in_direction(self, player, room, weapon, distance, direction):
        ''' Attack in direction; logic for what gets hit (door, room, or wall) goes here'''
        adj_room = room.get_in_direction(direction)

        # Are we going to hit a door?
        if adj_room.door is not None \
            and isinstance(adj_room.door, erukar.engine.environment.Door):
            if adj_room.door.status is not Door.Open:
                return 'You have attacked a door.'

        # are we actually able to hit the room in this direction (and does it exist?)
        if adj_room.room is not None:
            return self.attack_into_room(player, adj_room.room, weapon, distance+1, direction)
        return 'You attack a wall. Are you happy now?'

    def attack_into_room(self, player, room, weapon, distance, direction):
        '''Check to see if there's a target in this room to attack; attack if so'''
        if weapon.AttackRange >= distance:
            targets = [c for c in room.contents \
                       if isinstance(c, erukar.engine.lifeforms.Lifeform)]
            if len(targets) < 1:
                return self.attack_in_direction(player, room, weapon, distance, direction)

            # Actually Attack
            target = random.choice(targets)
            penalty = weapon.RangePenalty * distance
            return self.adjudicate_attack(player, weapon, target, penalty)

        return 'Your weapon does not have the range to attack {}.'.format(direction.name)

    def adjudicate_attack(self, subject, weapon, enemy, roll_penalty=0):
        '''Used to actually resolve an attack roll made between a character and target'''
        raw_attack_roll, armor_class, damages = self.calculate_attack(subject, weapon, enemy)
        attack_roll = raw_attack_roll - roll_penalty
        damage = sum([x[0] for x in damages]) # 0 is the index for the damage roll value
        damage_descriptions = ', '.join(["{} {}".format(*x) for x in damages])

        args = {
            'subject': subject.alias(),
            'target': enemy.alias(),
            'roll': attack_roll,
            'damage': damage_descriptions}

        if attack_roll <= armor_class:
            return Attack.unsuccessful.format(**args)

        enemy.take_damage(damage)
        attack_string = Attack.successful.format(**args)

        if hasattr(enemy, 'afflictions'):
            if enemy.afflicted_with(erukar.engine.afflictions.Dying):
                attack_string = attack_string + Attack.caused_dying.format(**args)

            if enemy.afflicted_with(erukar.engine.afflictions.Dead):
                self.create_corpse(enemy)
                attack_string = attack_string + Attack.caused_death.format(**args)

        return attack_string

    def create_corpse(self, target):
        room = target.current_room
        if target in room.contents:
            room.remove(target)
        room.add(Corpse(target))

    def calculate_attack(self, character, weapon, target):
        '''Involves the calculation of armor_class, attack roll, and damage'''
        armor_class = target.calculate_armor_class()
        if weapon is None:
            return [0, armor_class, 0]

        attack_roll = character.roll(character.stat_random_range('dexterity'))
        damage = weapon.roll(character)

        return [attack_roll, armor_class, damage]

