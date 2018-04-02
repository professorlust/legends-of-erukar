from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, joinedload

from erukar.system.data.ErukarBaseModel import *
import erukar

class Lifeform(ErukarBaseModel, Base):
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
    region      = Column(String)
    sector      = Column(String)
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

    sector      = Column(String, default='(0,0,0)')

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
        'instance',
        'region',
        'sector'
    ]

    def get_schema_query(session, id):
        return session.query(Lifeform)\
            .options(\
                joinedload(Lifeform.skills),\
                joinedload(Lifeform.equipment),\
                joinedload(Lifeform.inventory))\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = erukar.system.engine.Lifeform()
        self.map_schema_to_object(new_obj)
        return new_obj

    def map_schema_to_object(self, new_object):
        ErukarBaseModel.map_schema_to_object(self, new_object)
        self.map_inventory_on_object(new_object)
        self.map_skills_on_object(new_object)

    def map_location_to_object(self, new_object):
        new_object.sector = self.sector

    def map_inventory_on_object(self, new_object):
        for schema_item in self.inventory:
            # Below here can be added to Item
            real_item = schema_item.create_new_object()
            new_object.add_to_inventory(real_item)
            location = schema_item.equipment_location(self.equipment)
            if location: setattr(new_object, location, real_item)

    def map_skills_on_object(self, new_object):
        for schema_item in self.skills:
            real_skill = schema_item.create_new_object()
            new_object.skills.append(real_skill)

    def get(session, id):
        s_model = Lifeform.get_schema_query(session, id).first()
        return s_model.create_new_object()

    # Will need to rework this to prevent vulnerabilities from client-side
    def apply_template(self, template_json):
        self.apply_template_inventory(template_json)
        self.apply_template_skills(template_json)

    def apply_template_inventory(self, template_json):
        if 'inventory' not in template_json: return
        for item in template_json['inventory']:
            schema = erukar.system.data.Item()
            schema.item_type = item['type']
            if 'material' in item:
                schema.material_type = item['material']
            self.inventory.append(schema)
            if 'slot' in item:
                slot_schema = erukar.system.data.EquippedItem()
                slot_schema.item = schema
                slot_schema.equipment_slot = item['slot']
                self.equipment.append(slot_schema)

    def apply_template_skills(self, template_json):
        if 'skills' not in template_json: return
        for skill in template_json['skills']:
            schema = erukar.system.data.Skill()
            schema.skill_type = skill['type']
            schema.level = skill['level']
            self.skills.append(schema)
