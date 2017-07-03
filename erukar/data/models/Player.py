from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload

from erukar.data.SchemaBase import Base, ErukarBase
import erukar

class Player(ErukarBase, Base):
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

    def create_new_object(self):
        new_object = erukar.engine.model.PlayerNode(self.uid, None)
        self.map_schema_to_object(new_object)
        return new_object
