from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, joinedload

from erukar.data.SchemaBase import Base, ErukarBase
import erukar

class Lifeform(ErukarBase, Base):
    __tablename__ = 'lifeforms'
    __mapper_args_ = { 
        'polymorphic_identity': 'lifeforms',
        'polymorphic_on': type
    }

    id          = Column(Integer, primary_key=True)
    type        = Column(String(50))
    deceased    = Column(Boolean, default=False)
    max_health  = Column(Integer, default=4)
    name        = Column(String,  default="unnamed")
    instance    = Column(String)
    health      = Column(Integer, default=4)
    strength    = Column(Integer, default=0)
    dexterity   = Column(Integer, default=0)
    vitality    = Column(Integer, default=0)
    acuity      = Column(Integer, default=0)
    sense       = Column(Integer, default=0)
    resolve     = Column(Integer, default=0)

    wealth      = Column(Integer, default=0)
    level       = Column(Integer, default=1)
    experience  = Column(Integer, default=0)

    skills      = relationship("Skill", cascade="all, delete-orphan") 
    spell_words = relationship("SpellWord", cascade="all, delete-orphan")
    equipment   = relationship("EquippedItem", cascade="all, delete-orphan")
    inventory   = relationship("Item", cascade="all, delete-orphan")
    effects     = relationship("Effect", cascade="all, delete-orphan")

    SimpleMapParams = [
        'id',
        'name',
        'max_health',
        'health',
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve',
        'level',
        'experience',
        'wealth',
        'instance'
    ]

    def get_schema_query(session, id):
        return session.query(Lifeform)\
            .options(\
                joinedload(Lifeform.skills),\
                joinedload(Lifeform.equipment),\
                joinedload(Lifeform.inventory))\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = erukar.engine.lifeforms.Lifeform()
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        ErukarBase.map_schema_to_object(self, new_object)
        self.map_inventory_on_object(new_object)

    def map_inventory_on_object(self, new_object):
        for schema_item in self.inventory:
            # Below here can be added to Item
            real_item = schema_item.create_new_object()
            new_object.add_to_inventory(real_item)
            location = schema_item.equipment_location(self.equipment)
            if location: setattr(new_object, location, real_item)

    def get(session, id):
        s_model = Lifeform.get_schema_query(session, id).first()
        return s_model.create_new_object()
