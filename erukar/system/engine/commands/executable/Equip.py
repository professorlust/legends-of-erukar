from erukar.system.engine import Armor, Weapon, SearchScope
from ..ActionCommand import ActionCommand


class Equip(ActionCommand):
    NotFound = "Object cannot be equipped as it was not found"
    CannotEquip = "'{}' was found but cannot be equipped"
    MismatchedSlot = "Cannot equip {} at slot {}"
    NotEnoughPoints = 'Not enough action points to equip {} to {}'
    RebuildZonesOnSuccess = True
    Success = '{} equipped as {} successfully.'

    '''
    Requires:
        equipment_slot
        interaction_target
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        target = self.args.get('interaction_target', None)
        if not target:
            return self.fail(Equip.NotFound)
        slot = self.args.get('equipment_slot', None)
        if slot not in target.EquipmentLocations:
            return self.fail(Equip.CannotEquip.format(target.describe()))

        if slot in ['left', 'right']:
            if self.should_equip_on_two_handed():
                return self.equip_on_two_handed(target, slot)
        return self.equip_in_place(target, slot)

    def should_equip_on_two_handed(self):
        player = self.args.get('player_lifeform')
        left = player.left
        right = player.right
        return (left and left.RequiresTwoHands)\
            or (right and right.RequiresTwoHands)

    def equip_on_two_handed(self, target, slot):
        '''occurs when we're equipping an item that needs two hands'''
        player = self.args['player_lifeform']
        already_equipped = player.left or player.right
        err = self.check_cost(player, already_equipped, target)
        if err:
            return err

        self.remove_equipment(player, 'left')
        self.remove_equipment(player, 'right')
        setattr(player, slot, target)
        player.right = target
        self.log(player, self.Success.format(target.describe(), slot))
        return self.succeed()

    def equip_in_place(self, target, slot):
        '''Used when we're not equipping on top of a two-handed item'''
        player = self.args['player_lifeform']
        equipment = getattr(player, slot)
        err = self.check_cost(player, equipment, target)
        if err:
            return err

        self.do_equip(target)
        self.log(player, self.Success.format(target.describe(), slot))
        return self.succeed()

    def check_cost(self, player, equipment, target):
        slot = self.args['equipment_slot']
        cost = self.cost_to_equip(equipment, target)
        if player.action_points() < cost:
            return self.fail(Equip.NotEnoughPoints.format(
                equipment.describe(), slot))
        player.consume_action_points(cost)

    def cost_to_equip(self, equipped, to_equip):
        return 1

    def do_equip(self, equipment):
        slot = self.args['equipment_slot']
        target = self.args['interaction_target']
        player = self.args['player_lifeform']
        if isinstance(target, Weapon) and target.RequiresTwoHands:
            self.remove_for_two_handed()
        else:
            self.remove_equipment(player, slot)

        setattr(player, slot, target)
        self.dirty(player)

        target.on_equip(self)
        payload = {'uid': str(equipment.uuid)}
        self.add_to_outbox(player, 'equip', payload)

    def remove_for_two_handed(self):
        player = self.args['player_lifeform']
        for hand in ['left', 'right']:
            self.remove_equipment(player, hand)

    def remove_equipment(self, player, slot):
        equipment = getattr(player, slot)
        setattr(player, slot, None)
        if equipment:
            payload = {'slot': slot}
            self.add_to_outbox(player, 'unequip', payload)
            equipment.on_unequip(self)
