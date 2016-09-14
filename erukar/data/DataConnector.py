from .Schema import *
from erukar.engine.model.PlayerNode import PlayerNode
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
        '''Translate a PlayerNode into a Player Schema object and add it'''
        self.add(playernode_object, Player)

    def add(self, obj, schema_type, supplementary_data=None):
        '''
        Master Method for adding new data into the database. Dynamic; auto-gets the
        field values based on field names in the schema. If there are discrepancies,
        use supplementary_data as a dict to add additional information into the new obj
        '''
        obj_params = schema_type.__dict__
        schema_params = {x:getattr(obj,x) for x in obj_params \
                         if isinstance(obj_params[x],InstrumentedAttribute) if hasattr(obj, x)}
        print(schema_params)
        if isinstance(supplementary_data, dict):
            schema_params.update(supplementary_data)
        new_object = schema_type(**schema_params)
        self.session.add(new_object)
        self.session.commit()

    def get_player(self, filters):
        data = self.get(Player, filters).first()
        return PlayerNode(data.uid, None)

    def get(self, schema_type, filters):
        return self.session.query(schema_type).filter_by(**filters)
