from erukar.data.Schema import *
from erukar.data.Connector import Connector
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

class ConnectorFactory:
    def __init__(self, passwd="thisisnottherealpassword"):
        self.connection_string = "postgres+pygresql:///loedev"

    def establish_connection(self):
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_metadata(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return Connector(self.Session())
