from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload

from ..ErukarBaseModel import ErukarBaseModel, Base

class Region(ErukarBaseModel, Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    name = Column(String)
    sectors = relationship("Sector", cascade="all, delete-orphan") 
    SimpleMapParams = ['name', 'uid']

    def get_schema_query(session, uid):
        return session.query(Region)\
            .options(joinedload(Region.sectors))\
            .filter_by(uid=uid)

    def create_new_object(self):
        new_obj = erukar.system.engine.Region()
        self.map_data_to_object(new_obj)
        return new_obj

    def map_data_to_object(self, new_object):
        new_object.id = self.id
        ErukarBaseModel.map_schema_to_object(self, new_object)

    def create_from_object(session, region):
        data = Region.get_schema_query(session, region.uid).first()
        if not data: data = Region()

        data.copy_from_object(region)
        for sector in region.sectors:
            sector_data = Sector.create_from_object(session, sector)
            if sector_data: data.sectors.append(sector_data)
        return data
