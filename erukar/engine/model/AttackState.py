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

        self.is_projectile = False
        self.projectile_depth = 0
        self.attack_direction = None
        self.ammunition = None

    def use_unarmed(self):
        self.weapon = UnarmedStrike()

    def is_projectile(self):
        return not self.weapon or self.weapon.AttackRange > 0 and self.attack_direction is not None

    def origin(self):
        return self.attacker.current_room

    def get_weapon(self, equipment_slot, use_unarmed_if_none=False):
        if self.attacker:
            self.weapon = getattr(self.attacker, equipment_slot)
        self.weapon = UnarmedStrike() if (self.weapon is None and use_unarmed_if_none) else self.weapon

    def is_valid(self):
        return (self.weapon is not None and isinstance(self.weapon, Weapon)) and ((self.is_projectile and self.ammunition is not None) or (not self.is_projectile and self.target.current_room == self.attacker.current_room))

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
