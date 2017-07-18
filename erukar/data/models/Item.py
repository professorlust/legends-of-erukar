from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base, ErukarBase, SchemaLogger
import erukar

class Item(ErukarBase, Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    item_type       = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
    material_type   = Column(String)
    modifiers       = relationship("Modifier", cascade="all, delete-orphan")
    item_attributes = Column(JSON, nullable=True)

    SimpleMapParams = []

    def get_schema_query(session, id):
        return session.query(Item)\
            .options(joinedload(Item.modifiers))\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = ErukarBase.create_from_type(self.item_type)
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        new_object.id = self.id
        ErukarBase.map_schema_to_object(self, new_object)
        # Do stuff here with modifiers and attributes
        if self.material_type:
            self.apply_material(new_object)
        self.apply_modifiers(new_object)
        self.apply_attributes(new_object)

    def apply_material(self, new_object):
        material = ErukarBase.create_from_type(self.material_type)
        material.apply_to(new_object)

    def apply_modifiers(self, new_object):
        for modifier_schema in self.modifiers:
            modifier = modifier_schema.create_new_object()
            modifier.apply_to(new_object)

    def apply_attributes(self, new_object):
        if not self.item_attributes: return
        for attribute_name in self.item_attributes:
            setattr(new_object, attribute_name, self.item_attributes[attribute_name])

    def equipment_location(self, equipment):
        return next((x.equipment_slot for x in equipment if x.item_id == self.id), None)

    def get(session, id):
        s_model = Lifeform.get_schema_query(session, id).first()
        return s_model.create_new_object()

    def create_from_object(session, item):
        if hasattr(item, 'id'): 
            schema = Item.get_schema_query(session, item.id).first()
        else: schema = Item()
            
        if not schema:
            SchemaLogger.info('schema not loaded for item id {}'.format(getattr(item, 'id', -1)))
            raise Exception('schema not loaded for item id {}'.format(getattr(item, 'id', -1)))
        schema.item_type = item.__module__
        schema.copy_from_object(item)
        if item.material:
            schema.material_type = item.material.__module__
        for real_mod in item.modifiers:
            schema_mod = erukar.data.models.Modifier.create_from_object(session, real_mod)
            schema.modifiers.append(schema_mod)
        schema.attributes = item.persistable_attributes()
        return schema
