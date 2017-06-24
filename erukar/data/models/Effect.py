from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from erukar.data.SchemaBase import Base

class Effect(Base):
    __tablename__ = 'effects'

    id              = Column(Integer, primary_key=True)
    effect_type     = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
