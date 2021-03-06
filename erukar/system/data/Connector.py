from erukar.system.data.model import *
from erukar.system.data.ErukarBaseModel import Base
from sqlalchemy.orm import sessionmaker
import sqlalchemy, os

class Connector:
    def __init__(self,username="postgres",passwd="nottherealpass"):
        self.connection_string = os.environ.get('DATABASE_URL',"postgres+pygresql://{}:{}@localhost:5432/loedev".format(username, passwd))

    def establish_connection(self):
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_metadata(self):
        metadata = sqlalchemy.schema.MetaData(self.engine)
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
