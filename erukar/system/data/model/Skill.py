from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from ..ErukarBaseModel import ErukarBaseModel, Base

class Skill(ErukarBaseModel, Base):
    __tablename__ = 'skills'

    id              = Column(Integer, primary_key=True)
    skill_type      = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
    level           = Column(Integer, default=1)
    attributes      = Column(JSON, nullable=True)

    SimpleMapParams = ['level']

    def get_schema_query(session, id):
        return session.query(Skill)\
            .filter_by(id=id)

    def create_new_object(self):
        new_obj = ErukarBaseModel.create_from_type(self.skill_type)
        self.map_schema_to_object(new_obj)
        new_obj.id = self.id
        return new_obj

    def create_from_object(session, skill):
        schema = Skill()
        schema.copy_from_object(session, skill)
        return schema

    def copy_from_object(self, session, skill):
        super().copy_from_object(skill)
        self.level = skill.level
        self.skill_type = skill.__module__

    def map_schema_to_object(self, new_obj):
        new_obj.id = self.id
        new_obj.level = self.level
        self.apply_attributes(new_obj)

    def apply_attributes(self, new_obj):
        if not self.attributes: return
        for attribute_name in self.attributes:
            setattr(new_obj, attribute_name, self.attributes[attribute_name])

    def get(session, id):
        s_model = Skill.get_schema_query(session, id).first()
        return s_model.create_new_object()
