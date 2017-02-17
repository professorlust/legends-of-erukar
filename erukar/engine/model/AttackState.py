from erukar.engine.inventory.Weapon import Weapon
from erukar.engine.inventory.UnarmedStrike import UnarmedStrike

class AttackState:
    def __init__(self):
        self.attacker = None
        self.target = None
        self.weapon = None
        self.efficiency = 1.0

        self.attack_roll = 0
        self.processed_damage_result = None

        self.projectile_depth = 0
        self.attack_direction = None
        self.ammunition = None

    def use_unarmed(self):
        self.weapon = UnarmedStrike()

    def is_projectile(self):
        return self.weapon_exists() and self.weapon.AttackRange > 0

    def origin(self):
        '''gets the origin (the room the attacker is in)'''
        return self.attacker.current_room

    def get_weapon(self, equipment_slot, use_unarmed_if_none=False):
        '''Gets a weapon if it exists, otherwise gets an Unarmed Strike'''
        if self.attacker:
            self.weapon = getattr(self.attacker, equipment_slot)
        # return an Unarmed Strike or None
        self.weapon = UnarmedStrike() if (self.weapon is None and use_unarmed_if_none) else self.weapon

    def is_valid(self):
        '''Do we have a weapon? If so, confirm that it can be used in either ranged or melee'''
        return self.weapon_exists() and (self.is_ranged_valid() or self.is_melee_valid())

    def weapon_exists(self):
        return self.weapon is not None and isinstance(self.weapon, Weapon)

    def is_ranged_valid(self):
        '''Check to see if we're a projectile, and then check to see if we have ammo if we need it)'''
        return self.is_projectile() and (not self.weapon.RequiresAmmo or self.weapon.has_correct_ammo(self.ammunition))

    def is_melee_valid(self):
        '''Make sure that melee attacks only happen in this room'''
        return not self.is_projectile() and self.target.current_room == self.attacker.current_room

    def calculate_attack(self):
        '''Get the basic attack roll, then modify it based on the weapon and weapon mods'''
        self.weapon.on_attack(self)
        base_attack_roll = self.attacker.calculate_attack_roll(self.efficiency, self.target)
        modified_attack_roll = self.weapon.on_calculate_attack_roll(base_attack_roll, self.target)
        self.attack_roll = modified_attack_roll

    def attack_successful(self):
        '''Check to make sure that the attack bypassed the target's evasion'''
        return self.attack_roll >= self.target.evasion()

    def on_process_damage(self, command):
        '''Process a damage list against the target'''
        self.processed_damage_result = self.target.process_damage(self.weapon.damages, self.attacker, self.efficiency)
        self.attacker.on_process_damage(self, command)

    def add_extra_damage(self, damage):
        new_result = self.target.process_damage(damage, self.attacker)
        self.processed_damage_result.merge(new_result)

    def confirm(self):
        '''Actually apply the damage, incapacitate, and kill the target as calculated'''
        self.target.apply_damage(self.processed_damage_result, self.attacker)
