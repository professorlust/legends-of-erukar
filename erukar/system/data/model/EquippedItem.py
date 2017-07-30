from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from erukar.system.data.ErukarBaseModel import *

class EquippedItem(ErukarBaseModel, Base):
    __tablename__ = 'equippeditems'

    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    item_id         = Column(Integer, ForeignKey('items.id'), primary_key=True)
    item            = relationship("Item")
    equipment_slot  = Column(String)

    def get_schema_query(session, item_id, lifeform_id):
        return session.query(EquippedItem)\
            .filter_by(item_id=item_id, lifeform_id=lifeform_id)

    def get_specific_slot(session, equipment_slot, lifeform_id):
        return session.query(EquippedItem)\
            .filter_by(equipment_slot=equipment_slot, lifeform_id=lifeform_id)\
            .first()

    def create_from(session, player, slot, item):
        slot_schema = EquippedItem.get_specific_slot(session, slot, player.id)
        if not slot_schema:
            slot_schema = EquippedItem()
        slot_schema.equipment_slot = slot
        slot_schema.item = item
        return slot_schema
