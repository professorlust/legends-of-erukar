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
        l.link_to_room(r)

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
        p.uid = 'bob'
        pn = PlayerNode('bob', p)
        data = DataAccess()
        data.players.append(pn)
        p.link_to_room(r)
        pn.move_to_room(r)

        i = Inspect()
        i.sender_uid = 'bob'
        i.data = data
        i.execute()

        t = Take()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

        e = Equip()
        e.sender_uid = 'bob'
        e.user_specified_payload = 'sword'
        e.data = data
        e.execute()

        self.assertTrue(len(d.active_auras) > 0)

    def test_unequip_ends_aura(self):
        item = Sword()
        d = Dungeon()
        r = Room(d, (2,2))
        r.add(item)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        p = Player()
        p.uid = 'bob'
        pn = PlayerNode('bob', p)
        data = DataAccess()
        data.players.append(pn)
        p.link_to_room(r)
        pn.move_to_room(r)

        i = Inspect()
        i.sender_uid = 'bob'
        i.data = data
        i.execute()

        t = Take()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

        e = Equip()
        e.sender_uid = 'bob'
        e.user_specified_payload = 'sword'
        e.data = data
        e.execute()

        u = Unequip()
        u.sender_uid = 'bob'
        u.user_specified_payload = 'sword'
        u.data = data
        u.execute()

        self.assertTrue(len(list(x for x in d.active_auras if not x.is_expired)) == 0)

    def test_move_moves_auras(self):
        item = Sword()
        d = Dungeon()
        sr = Room(d, (0,0))
        nr = Room(d, (0,1))
        sr.add(item)
        sr.coestablish_connection(Direction.North, nr, None)

        f = erukar.game.modifiers.inventory.Glowing()
        f.apply_to(item)

        p = Player()
        p.uid = 'bob'
        p.current_room = sr
        pn = PlayerNode('bob', p)
        data = DataAccess()
        data.players.append(pn)
        p.link_to_room(sr)
        pn.move_to_room(sr)

        i = Inspect()
        i.sender_uid = 'bob'
        i.data = data
        i.execute()

        t = Take()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

        e = Equip()
        e.sender_uid = 'bob'
        e.user_specified_payload = 'sword'
        e.data = data
        e.execute()

        m = Move()
        m.sender_uid = 'bob'
        m.user_specified_payload = 'North'
        m.data = data
        m.execute()

        self.assertTrue(len(list(x for x in d.active_auras if not x.location.coordinates == (0,1))) == 0)

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
        pn = PlayerNode('bob', p)
        data = DataAccess()
        data.players.append(pn)
        p.link_to_room(r)
        pn.move_to_room(r)

        i = Inspect()
        i.sender_uid = 'bob'
        i.data = data
        i.execute()

        t = Take()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

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
        pn = PlayerNode('bob', p)
        data = DataAccess()
        data.players.append(pn)
        p.link_to_room(r)
        pn.move_to_room(r)

        i = Inspect()
        i.sender_uid = 'bob'
        i.data = data
        i.execute()

        t = Take()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

        t = Drop()
        t.user_specified_payload = 'sword'
        t.sender_uid = 'bob'
        t.data = data
        t.execute()

        self.assertEqual(len(list(x for x in d.active_auras if not x.is_expired)), 1)

