from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from erukar.data.models.Lifeform import Lifeform

class Creature(Lifeform):
    __tablename__ = 'creatures'
    __mapper_args_ = { 
        'polymorphic_identity': 'creatures',
    }

    id          = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    uid         = Column(String, nullable=False)
    str_ratio   = Column(Float, default=0.1667)
    dex_ratio   = Column(Float, default=0.1667)
    vit_ratio   = Column(Float, default=0.1667)
    acu_ratio   = Column(Float, default=0.1667)
    sen_ratio   = Column(Float, default=0.1667)
    res_ratio   = Column(Float, default=0.1667)
    elite_points= Column(Float, default=0.0)

    template    = Column(String)
    modifiers   = Column(ARRAY(String))
    history     = Column(ARRAY(String))
    region      = Column(String)
