from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, joinedload

from erukar.data.SchemaBase import SchemaLogger
from erukar.data.models.Lifeform import Lifeform
from erukar.engine.lifeforms.Player import Player
import erukar, sys

class Character(Lifeform):
    __tablename__ = 'characters'
    __mapper_args_ = { 
        'polymorphic_identity': 'characters',
    }

    id          = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    stat_points = Column(Integer, default=15)
    player_id   = Column(Integer, ForeignKey('players.id'), nullable=False)
    player      = relationship("Player", foreign_keys=[player_id])
    
    SimpleMapParams = [
        'name',
        'max_health',
        'health',
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve',
        'level',
        'experience',
        'wealth',
        'instance',
        'name',
    ]

    def get_schema_query(session, cid, uid=None, pid=None):
        if uid:
            node = erukar.data.models.Player.get(session, uid)
            return session.query(Character)\
                .options(\
                    joinedload(Lifeform.skills),\
                    joinedload(Lifeform.equipment),\
                    joinedload(Lifeform.inventory))\
                .filter_by(id=cid, player_id=node.id)

        return session.query(Character)\
            .options(\
                joinedload(Lifeform.skills),\
                joinedload(Lifeform.equipment),\
                joinedload(Lifeform.inventory))\
            .filter_by(id=cid, player_id=pid)

    def update(player, session):
        schema = Character.get_schema_query(session, player.id, pid=player.player_id).first()
        SchemaLogger.info(schema)
        if not schema:
            SchemaLogger.info('asdf')
            schema = Character()
            schema.player = erukar.data.models.Player.get(session, uid)

        schema.copy_from_object(session, player.lifeform())
        schema.add_or_update(session)

    def copy_inventory(self, session, player):
        schema_map = {}

        # Map all items in the inventory
        for item in player.inventory:
            schema_item = erukar.data.models.Item.create_from_object(session, item)
            schema_map[item] = schema_item
            self.inventory.append(schema_item)

        for slot in player.equipment_types:
            equipped_item = getattr(player, slot, None)
            if not equipped_item: continue
            schema_item = schema_map[equipped_item] 
            schema_equipment = erukar.data.models.EquippedItem.create_from(session, player, slot, schema_item)
            SchemaLogger.info('Appending {}'.format(schema_equipment))
            self.equipment.append(schema_equipment)

    def copy_from_object(self, session, player):
        super().copy_from_object(player)
        self.copy_inventory(session, player)

    def create_from_object(session, player, node_schema=None):
        schema = Character()
        if hasattr(player, 'id'):
            schema.id = player.id
        if hasattr(player, 'player_id'):
            schema.player_id = player.player_id
        else: schema.player = node_schema

        if not schema.id:
            SchemaLogger.info('adding!')
            schema.add_or_update(session)
            player.id = schema.id

        schema.copy_from_object(session, player)
        return schema

    def create_new_object(self):
        p = erukar.engine.lifeforms.Player()
        self.map_schema_to_object(p)
        p.id = self.id
        p.player_id = self.player_id
        return p

    def select(session, cid, uid):
        return Character.get_schema_query(session, cid, uid).first()
