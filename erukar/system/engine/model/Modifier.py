from .Describable import Describable
from erukar.system.engine import Rarity

class Modifier(Describable):
    NONE = 0
    NONE_PROHIBITED = 1
    ALL_PERMITTED_BUT_NOT_PROHIBITED = 2
    ALL_PERMITTED = 3
    ALL = 4

    Desirability = 0
    PermittedEntities = []
    ProhibitedEntities = []
    PermissionType = ALL
    DefaultPersistence = True

    PriceMultiplier = 1
    WeightMultiplier = 1
    MinimumDurabilityPriceMultiplier = 0.5

    InventoryName = '__class__'
    InventoryDescription = 'Basic inventory description for {__module__}'

    ShouldRandomizeOnApply = False
    PersistentAttributes = []

    ShowInAlias = False
    ShowInInventory = True
    ShowInEquipment = False

    def __init__(self):
        super().__init__()
        self.is_set = False
        self.applied_to = None
        self.persistent = self.DefaultPersistence
        self.rarity = Rarity.Mundane

    def modify(self, entity):
        '''Safe-guarded modification entry point'''
        if self.can_apply_to(entity):
            self.apply_to(entity)

    def apply_to(self, entity, parameters=None):
        '''Actually does the modification; this should be overridden'''
        self.applied_to = entity
        if not self.is_set and self.ShouldRandomizeOnApply:
            self.is_set = True
            self.randomize(parameters)

    def on_alias(self, current_alias):
        '''
        Used when formatting the alias for an item
        Helpful for materials (Steel + sword.alias()) or suffixes/prefixes from other modifiers
        (e.g. "Shoddy + (Steel Sword)" or "(Steel Sword) of the Flames"
        '''
        return current_alias

    def remove(self):
        '''Removes modification; this should be overridden'''
        pass

    def on_start(self, room):
        pass

    def on_take(self, lifeform):
        pass

    def on_drop(self, room, lifeform):
        pass

    def on_move(self, room):
        pass

    def on_equip(self, lifeform):
        pass

    def on_unequip(self, lifeform):
        pass

    @classmethod
    def can_apply_to(cls, item):
        for item_type in cls.PermittedEntities:
            if isinstance(item, item_type):
                return True
        return False

    def is_in_group(self, entity, group):
        '''
        Used to determine if the entity belongs to either the Permitted or
        the Prohibited Entities Lists
        '''
        return any(r for r in group if isinstance(entity, r))

    def on_calculate_attack_roll(self, current, target):
        return current

    def on_process_damage(self, attack_state, command):
        pass

    def on_calculate_attack_ranged(self, attack_state):
        pass

    def persistable_attributes(self):
        '''For use with database; getattrs all attributes defined by persistent_attr dict'''
        return {pattr: getattr(self, pattr) for pattr in self.PersistentAttributes if hasattr(self, pattr)}

    def get_additional_damages(self, weapon, is_attack=False):
        pass

    def modify_base_damage(self, damage, weapon):
        pass

    def post_successful_attack(self, cmd, attacker, weapon, target):
        pass

    def post_missed_attack(self, cmd, attacker, weapon, target):
        pass
