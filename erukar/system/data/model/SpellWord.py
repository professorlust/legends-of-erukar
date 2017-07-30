from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from erukar.system.data.ErukarBaseModel import Base

class SpellWord(Base):
    __tablename__ = 'spellwords'

    id              = Column(Integer, primary_key=True)
    word_class      = Column(String)
    successes       = Column(Integer)
    total           = Column(Integer)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
