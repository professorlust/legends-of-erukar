from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import JSON

from ..ErukarBaseModel import ErukarBaseModel, Base

class Sector(ErukarBaseModel, Base):
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String)

    '''
    Location is (X, alpha, beta) where...
        X is a location on the x-axis
        alpha is a location on the negatively-sloped diagonal
        beta is a location on the positively sloped diagonal
    '''
    x = Column(Integer)
    alpha = Column(Integer)
    beta = Column(Integer)

    environment_profile = Column(JSON)
    resource_profile = Column(JSON)
    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship("Region", foreign_keys=[region_id])
    locations = relationship("Location", cascade="all, delete-orphan") 

    SimpleMapParams = ['name', 'uid', 'x', 'alpha', 'beta']

    def coordinates(self):
        return (self.x, self.alpha, self.beta)

    def get_schema_query(session, uid):
        return session.query(Sector)\
            .filter_by(uid=uid)

    def create_new_object(self):
        new_obj = erukar.system.engine.Sector()
        self.map_data_to_object(new_obj)
        return new_obj

    def map_data_to_object(self, new_object):
        new_object.id = self.id
        ErukarBaseModel.map_schema_to_object(self, new_object)

    def create_from_object(session, sector):
        data = Sector.get_schema_query(session, sector.uid).first()
        if not data: data = Sector()

        data.copy_from_object(sector)
        for location in sector.locations:
            location_data = Location.create_from_object(session, location)
            if location_data: data.locations.append(location_data)
        return data
