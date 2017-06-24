from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from erukar.data.SchemaBase import Base

class Skill(Base):
    __tablename__ = 'skills'

    id              = Column(Integer, primary_key=True)
    skill_type      = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
    level           = Column(Integer, default=1)
    attributes      = Column(JSON, nullable=True)
