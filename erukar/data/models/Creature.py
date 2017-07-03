from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from erukar.data.models.Lifeform import Lifeform
from erukar.engine.lifeforms.Enemy import Enemy

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

    SimpleMapParams = [
        'name',
        'max_health',
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve',
        'level',
        'experience',
        'wealth',
        'str_ratio',
        'dex_ratio',
        'vit_ratio',
        'acu_ratio',
        'sen_ratio',
        'res_ratio',
        'elite_points',
        'uid',
        'template',
        'region'
    ]

    def get(session, uid):
        found_creature = session.query(Creature)\
            .options(joinedload(Creature.equipment), joinedload(Creature.inventory))\
            .filter_by(uid=uid, deceased=False)\
            .first()

        if not found_creature: return None
        return Creature.map_schema_to_object(found_creature, object_type=Enemy)

    def add(self, session):
        '''Takes an enemy object and maps it to a Creature Schema object, then persists'''
        session.add(self)
        session.commit()

    def create_from_object(existing_object):
        creature = Creature()
        creature.copy_from_object(existing_object)
        return creature

    def map_schema_to_object(self, existing_object=None):
        '''Map our properties onto an Enemy object'''
        if not existing_object: raise Exception('Creature Schema Object attempted to map a null object')
        super().map_schema_to_object(existing_object)
        existing_object.health = existing_object.max_health
