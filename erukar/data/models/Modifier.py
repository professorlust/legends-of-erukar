from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base

class Modifier(Base):
    __tablename__ = 'modifiers'

    id              = Column(Integer, primary_key=True)
    modifier_type   = Column(String)
    item_id         = Column(Integer, ForeignKey('items.id'))
    item            = relationship("Item", foreign_keys=[item_id])
    level           = Column(Integer)
    attributes      = Column(JSON, nullable=True)
