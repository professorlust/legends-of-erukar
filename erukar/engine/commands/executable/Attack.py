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

        if lifeform.weapon is None:
            return 'You must equip a weapon in order to attack'

        # Determine if this is directional attack
        direction = self.determine_direction(self.payload.lower())
        if direction is not None:
            room = lifeform.current_room
            return self.attack_in_direction(room, lifeform, 0, direction)

        # see if it's a target
        target = self.find_in_room(lifeform.current_room, self.payload)
        if target is not None:
            return self.adjudicate_attack(lifeform, target)
        return Attack.not_found.format(self.payload)

    def attack_in_direction(self, room, player, distance, direction):
        ''' Attack in direction; logic for what gets hit (door, room, or wall) goes here'''
        adj_room = room.get_in_direction(direction)

        # Are we going to hit a door?
        if adj_room.door is not None \
            and isinstance(adj_room.door, erukar.engine.environment.Door):
            if adj_room.door.status is not Door.Open:
                return 'You have attacked a door.'

        # are we actually able to hit the room in this direction (and does it exist?)
        if adj_room.room is not None:
            return self.attack_into_room(adj_room.room, player, distance+1, direction)

        return 'You attack a wall. Are you happy now?'

    def attack_into_room(self, room, player, distance, direction):
        if player.weapon.AttackRange >= distance:
            targets = [c for c in room.contents \
                       if isinstance(c, erukar.engine.lifeforms.Lifeform)]
            if len(targets) < 1:
                return self.attack_in_direction(room, player, distance, direction)

            # Actually Attack
            target = random.choice(targets)
            penalty = player.weapon.RangePenalty * distance
            return self.adjudicate_attack(player, target, penalty)

        return 'Your weapon does not have the range to attack {}.'.format(direction.name)

    def adjudicate_attack(self, subject, enemy, roll_penalty=0):
        '''Used to actually resolve an attack roll made between a character and target'''
        raw_attack_roll, armor_class, damages = self.calculate_attack(subject, enemy)
        attack_roll = raw_attack_roll - roll_penalty
        damage = sum([x[0] for x in damages])
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
            if 'dying' in enemy.afflictions:
                return attack_string + Attack.caused_dying.format(**args)

            if 'dead' in enemy.afflictions:
                self.create_corpse(enemy)
                return attack_string + Attack.caused_death.format(**args)

        return attack_string

    def create_corpse(self, target):
        '''Replaces a lifeform with a corpse'''
        room = target.current_room
        room.remove(target)
        room.add(Corpse(target))
    
    def calculate_attack(self, character, target):
        '''Attack another lifeform'''
        armor_class = target.calculate_armor_class()
        if character.weapon is None:
            return [0, armor_class, 0]

        attack_roll = character.roll(character.skill_range('dexterity'))
        damage = character.weapon.roll(character)

        return [attack_roll, armor_class, damage]

