from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from erukar.data.SchemaBase import Base

class EquippedItem(Base):
    __tablename__ = 'equippeditems'

    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    item_id         = Column(Integer, ForeignKey('items.id'), primary_key=True)
    item            = relationship("Item")
    equipment_slot  = Column(String)
