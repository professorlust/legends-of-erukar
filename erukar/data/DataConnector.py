from .Schema import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
import sqlalchemy

'''Establish'''
class DataConnector:
    def __init__(self, passwd="thisisnottherealpassword"):
        self.connection_string = "postgres+pygresql://postgres:{}@localhost:5432/loedev".format(passwd)

    def establish_connection(self):
        #engine = create_engine('sqlite:///:memory:', echo=True)
        self.engine = sqlalchemy.create_engine(self.connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_metadata(self):
        Base.metadata.create_all(self.engine)

    def add_player(self, playernode_object):
        supplementary_data = {'uid': playernode_object.uid}
        self.add(playernode_object, Player, supplementary_data)

    def add(self, obj, schema_type, supplementary_data=None):
        obj_params = type(obj).__dict__
        schema_params = {x:getattr(obj,x) for x in obj_params \
                         if isinstance(obj_params[x],InstrumentedAttribute) if hasattr(obj, x)}
        if supplementary_data and isinstance(supplementary_data, dict):
            schema_params.update(supplementary_data)
        new_object = schema_type(**schema_params)
        self.session.add(new_object)
        self.session.commit()


    def get_test_objects(self):
        return self.session.query(Character).filter_by(name="Vorenus").first()
