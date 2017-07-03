from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from erukar.data.models.Lifeform import Lifeform
from erukar.engine.lifeforms.Player import Player
import erukar

class Character(Lifeform):
    __tablename__ = 'characters'
    __mapper_args_ = { 
        'polymorphic_identity': 'characters',
    }

    id          = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    stat_points = Column(Integer, default=15)
    player_id   = Column(Integer, ForeignKey('players.id'), nullable=False)
    player      = relationship("Player", foreign_keys=[player_id])
    
    SimpleMapParams = [
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
        'name',
    ]

    def create_new_object(self):
        p = Player()
        self.map_schema_to_object(p)
        return p

    def select(session, cid, uid):
        node = erukar.data.models.Player.get(session, uid)
        return session.query(Character)\
            .filter_by(id=cid, player_id=node.id)\
            .first()
