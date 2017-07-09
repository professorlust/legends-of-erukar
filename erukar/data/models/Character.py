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
        'id',
        'player_id',
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
        for item in player.inventory:
            schema_item = erukar.data.models.Item.create_from_object(session, item)
            self.inventory.append(schema_item)

            for slot in player.equipment_types:
                equipped_item = getattr(player, slot, None)
                if item is equipped_item:
                    schema_equipment = erukar.data.models.EquippedItem.create_from(session, player, slot, schema_item)
                    self.equipment.append(schema_equipment)

    def copy_from_object(self, session, player):
        super().copy_from_object(player)
        self.copy_inventory(session, player)

    def create_from_object(player):
        schema = Character()
        schema.copy_from_object(player)
        return schema

    def create_new_object(self):
        p = erukar.engine.lifeforms.Player()
        self.map_schema_to_object(p)
        return p

    def select(session, cid, uid):
        return Character.get_schema_query(session, cid, uid).first()
