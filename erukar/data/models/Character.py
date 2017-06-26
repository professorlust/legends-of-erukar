from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from erukar.data.models.Lifeform import Lifeform
from erukar.engine.lifeforms.Player import Player

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

    def map_to_new_player(self):
        p = Player()
        for param in Character.SimpleMapParams:
            setattr(p, param, getattr(self, param))
        return p
