from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base, ErukarBase
import erukar

class Modifier(Base):
    __tablename__ = 'modifiers'

    id              = Column(Integer, primary_key=True)
    modifier_type   = Column(String)
    item_id         = Column(Integer, ForeignKey('items.id'))
    item            = relationship("Item", foreign_keys=[item_id])
    level           = Column(Integer)
    attributes      = Column(JSON, nullable=True)

    SimpleMapParams = ['level']

    def apply_attributes(self, new_object):
        if not self.attributes: return
        for attribute_name in self.attributes:
            setattr(new_object, attribute_name, self.attributes[attribute_name])

    def create_new_object(self):
        new_obj = ErukarBase.create_from_type(self.modifier_type)
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        ErukarBase.map_schema_to_object(self, new_object)
        self.apply_attributes(new_object)
        new_object.is_set = True
