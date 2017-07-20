from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base, ErukarBase, SchemaLogger

class Skill(ErukarBase, Base):
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
        new_obj = ErukarBase.create_from_type(self.skill_type)
        self.map_schema_to_object(new_obj)
        return new_obj

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
