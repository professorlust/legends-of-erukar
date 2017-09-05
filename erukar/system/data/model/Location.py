from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import JSON

from ..ErukarBaseModel import ErukarBaseModel, Base

class Location(ErukarBaseModel, Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String)

    environment_profile = Column(JSON)
    resource_profile = Column(JSON)

    sector_id = Column(Integer, ForeignKey('sectors.id'))
    sector = relationship("Sector", foreign_keys=[sector_id])

    SimpleMapParams = ['name', 'uid']

    def get_schema_query(session, uid):
        return session.query(Location)\
            .filter_by(uid=uid)

    def create_new_object(self):
        new_obj = erukar.system.engine.Location()
        self.map_data_to_object(new_obj)
        return new_obj

    def map_data_to_object(self, new_object):
        new_object.id = self.id
        ErukarBaseModel.map_schema_to_object(self, new_object)

    def create_from_object(session, location):
        data = Region.get_schema_query(session, region.uid).first()
        if not data: data = Location()

        data.copy_from_object(location)
        return data
