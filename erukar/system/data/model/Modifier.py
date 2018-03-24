from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from ..ErukarBaseModel import ErukarBaseModel, Base
import erukar

class Modifier(ErukarBaseModel, Base):
    __tablename__ = 'modifiers'

    id              = Column(Integer, primary_key=True)
    modifier_type   = Column(String)
    item_id         = Column(Integer, ForeignKey('items.id'))
    item            = relationship("Item", foreign_keys=[item_id])
    level           = Column(Integer)
    attributes      = Column(JSON, nullable=True)

    SimpleMapParams = ['level']

    def get_schema_query(session, id):
        return session.query(Modifier)\
            .filter_by(id=id)

    def apply_attributes(self, new_object):
        if not self.attributes: return
        for attribute_name in self.attributes:
            setattr(new_object, attribute_name, self.attributes[attribute_name])

    def create_new_object(self):
        new_obj = ErukarBaseModel.create_from_type(self.modifier_type)
        new_obj.id = self.id
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        ErukarBaseModel.map_schema_to_object(self, new_object)
        self.apply_attributes(new_object)
        new_object.is_set = True

    def create_from_object(session, existing):
        if hasattr(existing, 'id'):
            schema = Modifier.get_schema_query(session, existing.id).first()
        else: schema = Modifier()
        schema.level = getattr(existing, 'level', 0)
        schema.modifier_type = existing.__module__
        schema.attributes = existing.persistable_attributes()
        return schema
