from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from erukar.data.SchemaBase import Base

class Player(Base):
    __tablename__ = 'players'

    id          = Column(Integer, primary_key=True)
    uid         = Column(String, nullable=False)
    name        = Column(String)
    characters  = relationship("Character")
