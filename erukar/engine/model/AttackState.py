from erukar.engine.inventory.Weapon import Weapon
from erukar.engine.inventory.UnarmedStrike import UnarmedStrike

class AttackState:
    def __init__(self):
        self.attacker = None
        self.target = None
        self.weapon = None
        self.efficiency = 1.0

        self.attack_roll = 0
        self.damage_result = None

        self.projectile_depth = 0
        self.attack_direction = None
        self.ammunition = None

    def use_unarmed(self):
        self.weapon = UnarmedStrike()

    def is_projectile(self):
        return self.weapon_exists() and self.weapon.AttackRange > 0

    def origin(self):
        return self.attacker.current_room

    def get_weapon(self, equipment_slot, use_unarmed_if_none=False):
        if self.attacker:
            self.weapon = getattr(self.attacker, equipment_slot)
        self.weapon = UnarmedStrike() if (self.weapon is None and use_unarmed_if_none) else self.weapon

    def is_valid(self):
        return self.weapon_exists() and (self.is_ranged_valid() or self.is_melee_valid())

    def weapon_exists(self):
        return self.weapon is not None and isinstance(self.weapon, Weapon)

    def is_ranged_valid(self):
        return self.is_projectile and (self.ammunition is not None or not self.weapon.RequiresAmmo)

    def is_melee_valid(self):
        return not self.is_projectile and self.target.current_room == self.attacker.current_room

    def calculate_attack(self):
        self.attack_roll = self.attacker.calculate_attack_roll(self.efficiency, self.target)
        self.attack_roll = self.weapon.on_calculate_attack_roll(self.attack_roll, self.target)

    def attack_successful(self):
        return self.attack_roll >= self.target.evasion()

    def on_apply_damage(self, command):
        self.damage_result = self.target.apply_damage(self.weapon.damages, self.attacker, self.efficiency)
        self.attacker.on_apply_damage(self, command)

    def add_extra_damage(self, damage):
        new_result = self.target.apply_damage(damage, self.attacker)
        self.damage_result.merge(new_result)
