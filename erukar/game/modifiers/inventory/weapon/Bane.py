from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Damage import Damage
from erukar.engine.model.enum.Rarity import Rarity
import erukar, random

class Bane(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['damage_increase', 'target_type', 'InventoryDescription', 'InventoryName']

    Types = [
        'Undead',
        'Dragon',
        'Demon',
        'Construct',
        'Elemental',
        'Human'
    ]

    Levels = [
        'Minor',
        '',
        'Major',
        'Epic',
#       'Legendary',
#       'Mythical'
    ]

    def randomize(self, parameters=None):
        '''In the future we will determine level based on the generation parameters level and desirability''' 
        self.level = int(random.random() * len(self.Levels))
        

        self.damage_increase = 0.075 * (self.level + 1)
        self.target_type = random.choice(self.Types)
        self.InventoryName = '{} {}bane'.format(self.Levels[self.level], self.target_type).strip()
        self.InventoryDescription = 'Deals {:2.0f}% extra damage to any {}'.format(self.damage_increase*100, self.target_type)

    def on_process_damage(self, attack_state, command):
        '''Check to see if the enemy is of a specific type'''
        if not hasattr(self, 'target_class') or not self.target_class:
            self.target_class = getattr(erukar.game.enemies.templates, self.target_type)
        if isinstance(attack_state.target, self.target_class):
            self.do_bane(attack_state, command)

    def do_bane(self, attack_state, command):
        '''Do extra damage'''
        extra_damage = attack_state.processed_damage_result.get_damage_total() * self.damage_increase
        damage = Damage(
            "unmitigable",
            (extra_damage, extra_damage),
            'resolve',
            dist_and_params=(random.uniform, (0,1))
        )
        attack_state.add_extra_damage([damage])
