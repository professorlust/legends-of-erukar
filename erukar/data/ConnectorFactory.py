from erukar.data.models import *
from erukar.data.Connector import Connector
from erukar.data.SchemaBase import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy, os

class ConnectorFactory:
    def __init__(self,username="postgres",passwd="nottherealpass"):
        self.connection_string = os.environ.get('DATABASE_URL',"postgres+pygresql://{}:{}@localhost:5432/loedev".format(username, passwd))

    def establish_connection(self):
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_metadata(self):
        metadata = sqlalchemy.schema.MetaData(self.engine)
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return Connector(self.Session())
