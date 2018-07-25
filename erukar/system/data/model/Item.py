from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import JSON
from .Modifier import Modifier

from .Lifeform import Lifeform
from ..ErukarBaseModel import ErukarBaseModel, Base


class Item(ErukarBaseModel, Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    item_type = Column(String)
    lifeform_id = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform = relationship("Lifeform", foreign_keys=[lifeform_id])
    material_type = Column(String)
    durability = Column(Integer)
    modifiers = relationship("Modifier", cascade="all, delete-orphan")
    item_attributes = Column(JSON, nullable=True)

    SimpleMapParams = []

    def get_schema_query(session, id):
        return session.query(Item)\
            .options(joinedload(Item.modifiers))\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = ErukarBaseModel.create_from_type(self.item_type)
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        new_object.id = self.id
        ErukarBaseModel.map_schema_to_object(self, new_object)
        # Do stuff here with modifiers and attributes
        if self.material_type:
            self.apply_material(new_object)
        self.apply_modifiers(new_object)
        self.apply_attributes(new_object)

    def apply_material(self, new_object):
        material = ErukarBaseModel.create_from_type(self.material_type)
        material.apply_to(new_object)

    def apply_modifiers(self, new_object):
        for modifier_schema in self.modifiers:
            modifier = modifier_schema.create_new_object()
            modifier.apply_to(new_object)

    def update_attributes(self, item, session):
        self.item_attributes = item.persistable_attributes()
        self.add_or_update(session)

    def apply_attributes(self, new_object):
        if not self.item_attributes:
            return
        for _att in self.item_attributes:
            setattr(new_object, _att, self.item_attributes[_att])

    def equipment_location(self, equipment):
        for item in equipment:
            if item.item_id == self.id:
                return item.equipment_slot
        return None

    def get(session, id):
        s_model = Lifeform.get_schema_query(session, id).first()
        return s_model.create_new_object()

    def create_from_object(session, item):
        if hasattr(item, 'id'):
            schema = Item.get_schema_query(session, item.id).first()
        else:
            schema = Item()
        if not schema:
            _id = getattr(item, 'id', -1)
            raise Exception('schema not loaded for item id {}'.format(_id))
        schema.item_type = item.__module__
        schema.copy_from_object(item)
        if item.material:
            schema.material_type = item.material.__module__
        for real_mod in item.modifiers:
            schema_mod = Modifier.create_from_object(session, real_mod)
            schema.modifiers.append(schema_mod)
        schema.item_attributes = item.persistable_attributes()
        return schema
