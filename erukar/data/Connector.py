from .Schema import *
from erukar.engine.model.PlayerNode import PlayerNode
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
import sqlalchemy, erukar

'''Establish'''
class Connector:
    simple_map_character_params = ['name','max_health','health','strength','dexterity','vitality','acuity','sense','resolve','level','experience']
    def __init__(self, session):
        self.session = session

    def add(self, obj, schema_type, supplementary_data=None):
        '''
        Master Method for adding new data into the database. Dynamic; auto-gets the
        field values based on field names in the schema. If there are discrepancies,
        use supplementary_data as a dict to add additional information into the new obj
        '''
        schema_params = self.gen_to_dict(self.schema_params(obj, schema_type))
        if isinstance(supplementary_data, dict):
            schema_params.update(supplementary_data)
        new_object = schema_type(**schema_params)
        self.session.add(new_object)
        self.session.commit()

    def get(self, schema_type, filters):
        return self.session.query(schema_type).filter_by(**filters)

    '''Schema Specific CRUD'''
    def get_player(self, filters):
        data = self.get(Player, filters).first()
        return PlayerNode(data.uid, None)

    def get_character(self, uid):
        player = self.get(Player, {'uid': uid}).first()
        if player is None:
            return None
        return self.session.query(Character)\
                .options(joinedload(Character.equipment), joinedload(Character.inventory))\
                .filter_by(deceased=False)\
                .first();

    def update_character(self, character):
        if not hasattr(character, 'uid'): return
        schema = self.get_character(character.uid)
        if schema is None: return
        # Actually try to update the character
        inventory = self.gen_to_dict(self.generate_inventory(character))
        for schema_param in self.simple_map_character_params:
            setattr(schema, schema_param, getattr(character, schema_param))
        if character.health <= 0:
            schema.deceased = True
        schema.equipment = list(self.generate_equipped_items(character, inventory))
        schema.inventory = list(inventory.values())
        self.session.add(schema)
        self.session.commit()

    def load_player(self, uid, out_char):
        data = self.get_character(uid)
        if data is not None:
            self.simple_map_character(out_char, data)
            self.map_items_on_character(out_char, data)
        return data is not None

    def simple_map_character(self, out, data):
        '''Handles non-relational mapping onto an instantiated lifeform'''
        to_map = self.simple_map_character_params
        for x in to_map:
            setattr(out, x, getattr(data, x))

    def map_items_on_character(self, out, data):
        '''Create items from Schema and assign to inventory (or equipment slots as necessary)'''
        for item in data.inventory:
            instantiated = self.create_item(item)
            out.inventory.append(instantiated)
            # Now check to see if this item is equipped and if so, assign it to its spot
            location = next((x.equipment_slot for x in data.equipment if x.item_id == item.id ), None)
            if location is not None:
                setattr(out, location, instantiated)

    def create_item(self, data):
        '''Create an item from an ItemSchema'''
        return getattr(__import__(data.item_type), data.item_type.split('.')[-1])()

    def add_player(self, playernode_object):
        '''Translate a PlayerNode into a Player Schema object and add it'''
        self.add(playernode_object, Player)

    def add_character(self, playernode_object, lifeform_object):
        '''Used when adding a Lifeform to the database'''
        player = self.get(Player, {'uid': playernode_object.uid}).first()
        inventory = self.gen_to_dict(self.generate_inventory(lifeform_object))
        equipment = list(self.generate_equipped_items(lifeform_object, inventory))
        supplementary_data = {'player_id': player.id, 'inventory': list(inventory.values()), 'equipment': equipment}
        self.add(lifeform_object, Character, supplementary_data)

    def schema_params(self, obj, schema_type):
        '''Used to map to and from object to schema type'''
        obj_params = schema_type.__dict__
        for x in obj_params:
            if isinstance(obj_params[x],InstrumentedAttribute) and hasattr(obj, x):
                yield (x, getattr(obj,x))

    def generate_inventory(self, lifeform):
        '''Create Item Schema objects from a lifeform's inventory'''
        for item in lifeform.inventory:
            if item.Persistent:
                yield (item, erukar.data.Schema.Item(item_type=item.__module__))

    def gen_to_dict(self, generator):
        return {x[0]:x[1] for x in generator}

    def generate_equipped_items(self, character, inventory):
        '''Generator which matches the Inventory IDs against equipped slots'''
        for equip_slot in erukar.engine.lifeforms.Lifeform.equipment_types:
            equipped_item = getattr(character, equip_slot)
            if equipped_item in inventory:
                yield erukar.data.Schema.EquippedItem(equipment_slot=equip_slot, item=inventory[equipped_item])
