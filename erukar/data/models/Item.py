from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base, ErukarBase
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

    def get_schema_query(session, id):
        return session.query(Item)\
            .options(joinedload(Item.modifiers))\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = ErukarBase.create_from_type(self.item_type)
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        ErukarBase.map_schema_to_object(self, new_object)
        # Do stuff here with modifiers and attributes

    def equipment_location(self, equipment):
        return next((x.equipment_slot for x in equipment if x.item_id == self.id), None)

    def get(session, id):
        s_model = Lifeform.get_schema_query(session, id).first()
        return s_model.create_new_object()
