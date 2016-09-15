from erukar.data.Connector import Connector
from sqlalchemy.orm import sessionmaker
import sqlalchemy

class ConnectorFactory:
    def __init__(self, passwd="thisisnottherealpassword"):
        self.connection_string = "postgres+pygresql://postgres:{}@localhost:5432/loedev".format(passwd)

    def establish_connection(self):
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_metadata(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return Connector(self.Session())
