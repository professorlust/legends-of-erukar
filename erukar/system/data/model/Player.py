from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload

from erukar.system.data.ErukarBaseModel import *
from erukar.system.engine import PlayerNode

class Player(ErukarBaseModel, Base):
    __tablename__ = 'players'

    id          = Column(Integer, primary_key=True)
    uid         = Column(String, nullable=False)
    name        = Column(String)
    characters  = relationship("Character")

    SimpleMapParams = ['uid','name']

    def get_schema_query(session, uid):
        return session.query(Player)\
            .options(joinedload(Player.characters))\
            .filter_by(uid=uid)

    def get(session, uid):
        return Player.get_schema_query(session, uid).first()

    def add(session, playernode):
        schema = Player()
        schema.copy_from_object(playernode) 
        schema.add_or_update(session)
        return schema

    def create_new_object(self):
        new_object = PlayerNode(self.uid, None)
        self.map_schema_to_object(new_object)
        return new_object
