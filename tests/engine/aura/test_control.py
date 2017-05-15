from erukar import *
import erukar
import unittest

class AuraControlTests(unittest.TestCase):
    def test_room_can_create(self):
        d = Dungeon()
        r = Room(d, (0,0))

        aura = Aura((-2,-2))
        r.initiate_aura(aura)

        self.assertIn(aura, d.active_auras)
        self.assertEqual(aura.location.coordinates, (0,0))

    def test_lifeform_can_create(self):
        d = Dungeon()
        l = Lifeform()
        r = Room(d, (2,2))
        l.on_move(r)

        aura = Aura((-2,-2))
        l.initiate_aura(aura)

        self.assertIn(aura, d.active_auras)
        self.assertEqual(aura.location.coordinates, (2,2))

    def test_equip_starts_aura(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (2,2))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        p = Player()
        p.reserved_action_points = 2
        p.current_action_points = 2
        p.room = r
        p.world = d
        r.add(p)

        i = Inspect()
        i.world = d
        i.player_info = p
        inspect_result = i.execute()
        self.assertTrue(inspect_result.success)
        p.index_item(item, r)

        t = Take()
        t.args = {'interaction_target': item.uuid}
        t.world = d
        t.player_info = p
        take_result = t.execute()
        self.assertTrue(take_result.success)
        self.assertIn(item, p.inventory)

        e = Equip()
        e.world = d
        e.player_info = p
        e.args = {'interaction_target': item.uuid, 'equipment_slot': 'right'}
        res = e.execute()

        self.assertTrue(len(d.active_auras) > 0)

    def test_unequip_ends_aura(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (2,2))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        p = Player()
        p.current_action_points = 10
        p.room = r
        p.world = d
        r.add(p)

        i = Inspect()
        i.world = d
        i.player_info = p
        inspect_result = i.execute()
        self.assertTrue(inspect_result.success)
        p.index_item(item, r)

        t = Take()
        t.args = {'interaction_target': item.uuid}
        t.world = d
        t.player_info = p
        take_result = t.execute()
        self.assertTrue(take_result.success)
        self.assertIn(item, p.inventory)

        e = Equip()
        e.world = d
        e.player_info = p
        e.args = {'interaction_target': item.uuid, 'equipment_slot': 'right'}
        res = e.execute()
        self.assertEqual(item, p.right)
        self.assertTrue(res.success)

        ue = Unequip()
        ue.world = d
        ue.player_info = p
        ue.args = {'inventory_item': str(item.uuid)}
        res = ue.execute()
        self.assertTrue(res.success)

        self.assertTrue(len(list(x for x in d.active_auras if not x.is_expired)) == 0)

    def test_move_moves_auras(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (2,2))
        r.add(item)
        nr = Room(d, (0,1))
        nr.connect(r)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        p = Player()
        p.room = r
        p.world = d
        r.add(p)

        p.current_action_points = 20
        i = Inspect()
        i.world = d
        i.player_info = p
        inspect_result = i.execute()
        self.assertTrue(inspect_result.success)
        p.index_item(item, r)

        t = Take()
        t.args = {'interaction_target': str(item.uuid)}
        t.world = d
        t.player_info = p
        take_result = t.execute()
        self.assertTrue(take_result.success)
        self.assertIn(item, p.inventory)

        e = Equip()
        e.world = d
        e.player_info = p
        e.args = {'interaction_target': item.uuid, 'equipment_slot': 'right'}
        res = e.execute()

        m = Move()
        m.world = d
        m.player_info = p
        m.args = {'passage': r.connections[0].uuid}
        move_result = m.execute()
#       self.assertTrue(move_result.success)

#       self.assertEqual(len(list(x for x in d.active_auras if not x.location.coordinates == (0,1))), 0)
#       self.assertEqual(len(list(x for x in d.active_auras if x.location.coordinates == (0,1))), 1)

    def test_on_start_starts_auras(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (0,0))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        r.on_start()

        self.assertTrue(len(d.active_auras) > 0)

    def test_take_stops_started_aura(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (0,0))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)
        r.on_start()

        p = Player()
        p.uid = 'bob'
        p.current_room = r
        p.on_move(r)

        p.index_item(item, r)
        p.current_action_points = 20

        t = Take()
        t.args = {'interaction_target': item.uuid}
        t.world = d
        t.player_info = p
        self.assertTrue(t.execute().success)

        self.assertEqual(len(list(x for x in d.active_auras if not x.is_expired)), 0)

    def test_drop_restarts_aura(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (0,0))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)
        r.on_start()

        p = Player()
        p.uid = 'bob'
        p.current_room = r
        p.on_move(r)

        p.index_item(item, r)
        p.current_action_points = 20

        t = Take()
        t.args = {'interaction_target': item.uuid}
        t.world = d
        t.player_info = p
        self.assertTrue(t.execute().success)

        t = Drop()
        t.args = {'inventory_item': item.uuid}
        t.world = d
        t.player_info = p
        res = t.execute()
        self.assertTrue(res.success)
        self.assertIn(item, r.contents)

        self.assertEqual(len(list(x for x in d.active_auras if not x.is_expired)), 1)

