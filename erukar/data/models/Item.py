from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base

class Item(Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    item_type       = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
    material_type   = Column(String)
    modifiers       = relationship("Modifier", cascade="all, delete-orphan")
    item_attributes = Column(JSON, nullable=True)
