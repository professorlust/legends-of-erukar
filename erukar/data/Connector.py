from .Schema import *
from erukar.engine.magic.SpellWordGrasp import SpellWordGrasp
from erukar.engine.model.PlayerNode import PlayerNode
from sqlalchemy.orm import joinedload, load_only
from sqlalchemy.orm.attributes import InstrumentedAttribute
import sqlalchemy, erukar

'''Establish'''
class Connector:
    simple_map_lifeform_params = [
        'name',
        'max_health',
        'health',
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve',
        'level',
        'experience',
        'wealth',
        'instance'
    ]
    simple_map_creature_params = [
        'str_ratio',
        'dex_ratio',
        'vit_ratio',
        'acu_ratio',
        'sen_ratio',
        'res_ratio',
        'elite_points',
        'uid'
    ]
    simple_map_player_params = [
        'stat_points',
    ]

    def __init__(self, session):
        self.session = session

    def add(self, obj, schema_type, supplementary_data=None):
        '''
        Master Method for adding new data into the database. Dynamic; auto-gets the
        field values based on field names in the schema. If there are discrepancies,
        use supplementary_data as a dict to add additional information into the new obj
        '''
        schema_params = Connector.gen_to_dict(self.schema_params(obj, schema_type))
        if isinstance(supplementary_data, dict):
            schema_params.update(supplementary_data)
        new_object = schema_type(**schema_params)
        self.session.add(new_object)
        self.session.commit()

    def get(self, schema_type, filters):
        return self.session.query(schema_type).filter_by(**filters)

    def player_exists(self, uid):
        return self.get(Player, {'uid': uid}).first() is not None

    '''Schema Specific CRUD'''
    def get_player(self, filters):
        data = self.get(Player, filters)\
            .options(joinedload(Player.characters))\
            .first()
        pn = None if not data else PlayerNode(data.uid, None)
        characters = [] if not pn else data.characters
        return pn, characters

    def get_characters(self, playernode):
        return self.session.query(Character)\
            .all()

    def get_character(self, uid):
        print('getting character')
        player = self.get(Player, {'uid': uid}).first()
        if player is None:
            return None
        return self.session.query(Character)\
                .filter_by(player_id=player.id)\
                .options(joinedload(Character.equipment), joinedload(Character.inventory))\
                .filter_by(deceased=False)\
                .first();

    def get_creature(self, uid):
        creature = self.get(Creature, {'uid': uid}).first()
        if creature is None:
            # Simple ADD 
            self.session.add(Creature(uid=uid))
            self.session.commit()
        first = self.session.query(Creature)\
                .options(joinedload(Creature.equipment), joinedload(Creature.inventory))\
                .filter_by(uid=uid, deceased=False)\
                .first();
        return first

    def is_persistible_enemy(target):
        return isinstance(target, erukar.engine.lifeforms.Enemy) and not target.is_transient

    def get_lifeform_schema(self, target):
        '''Determines whether this is a Character, Creature, or neither'''
        if isinstance(target, erukar.engine.lifeforms.Player):
            return self.get_character(target.uid)
        if Connector.is_persistible_enemy(target):
            schema = self.get_creature(target.uid)
            return schema
        
    def map_list_of_parameters_to_schema(schema, target, parameter_list):
        '''Uses a list of parameters to perform a simple map'''
        for schema_param in parameter_list:
            setattr(schema, schema_param, getattr(target, schema_param))

    def map_lifeform_to_schema(self, target, schema):
        '''Performs basic Lifeform mapping, then uses polymorphism on remaining fields'''
        inventory = Connector.gen_to_dict(Connector.generate_inventory(target))
        schema.effects = list(Connector.generate_effects(target))

        # Set all of the SIMPLE MAP schema parameters on the out-object (character)
        Connector.map_list_of_parameters_to_schema(schema, target, Connector.simple_map_lifeform_params)

        # Now do complex mapping on equipment
        schema.equipment = list(Connector.generate_equipped_items(target, inventory))
        schema.inventory = list(inventory.values())
        if target.health <= 0:
            schema.deceased = True

        schema.spell_words = list(Connector.generate_words(target))

        # Polymorphism Mapping
        if isinstance(target, erukar.engine.lifeforms.Player):
            Connector.map_player_to_schema(target, schema)
        elif self.is_persistible_enemy(target):
            Connector.map_enemy_to_schema(target, schema)

    def map_enemy_to_schema(target,schema):
        '''Enemy-Specific, Polymorphic mapping'''
        Connector.map_list_of_parameters_to_schema(schema, target, Connector.simple_map_creature_params)
        schema.template = target.__module__
        schema.history = target.history
        schema.modifiers = [x.__module__ for x in target.modifiers]

    def map_player_to_schema(target,schema):
        '''Player-Specific, Polymorphic mapping'''
        Connector.map_list_of_parameters_to_schema(schema, target, Connector.simple_map_player_params)

    def load_player(self, uid, out_char):
        data = self.get_character(uid)
        if data is not None:
            Connector.simple_map_character(out_char, data)
            Connector.map_items_on_character(out_char, data)
            Connector.map_effects_on_character(out_char, data)
            Connector.map_words_on_character(out_char, data)
            Connector.map_skills_on_character(out_char, data)
        return data is not None

    def get_creature_uids(self):
        return self.session.query(Creature).options(load_only("uid")).all()

    def load_creature(self, uid):
        '''Creates a creature that has been persisted'''
        data = self.get_creature(uid)
        if data is None: return None
        out = self.create_from_type(data.template)
        if data is not None:
            Connector.simple_map_creature(out, data)
            self.map_items_on_character(out, data)
            self.map_effects_on_character(out, data)
            Connector.map_words(out_char, data)
        return out

    def simple_map_character(out, data):
        '''Handles non-relational mapping onto an instantiated lifeform'''
        to_map = Connector.simple_map_lifeform_params + Connector.simple_map_player_params
        for x in to_map:
            setattr(out, x, getattr(data, x))
            
    def simple_map_creature(out, data):
        '''Handles non-relational mapping onto an instantiated lifeform'''
        to_map = Connector.simple_map_lifeform_params + Connector.simple_map_creature_params
        for x in to_map:
            setattr(out, x, getattr(data, x))

    def map_words_on_character(out_char, data):
        '''Map Words from data onto character'''
        for word in data.spell_words:
            instantiated = SpellWordGrasp(word.word_class, word.successes, word.total)
            out_char.spell_words.append(instantiated)

    def map_effects_on_character(out, data):
        '''Create persistent effects from Schema and assign to the character'''
        for effect in data.effects:
            instantiated = Connector.create_from_type(effect.effect_type, args={'target': out})
            out.conditions.append(instantiated)

    def map_items_on_character(out, data):
        '''Create items from Schema and assign to inventory (or equipment slots as necessary)'''
        for item in data.inventory:
            instantiated = Connector.instantiate_item(item)
            out.add_to_inventory(instantiated)
            # Now check to see if this item is equipped and if so, assign it to its spot
            location = next((x.equipment_slot for x in data.equipment if x.item_id == item.id ), None)
            if location is not None:
                setattr(out, location, instantiated)
                
    def map_skills_on_character(out, data):
        '''Create persistent effects from Schema and assign to the character'''
        for skill in data.skills:
            instantiated = Connector.create_from_type(skill.skill_type)
            out.skills.append(instantiated)

    def instantiate_item(data):
        '''Create an item from an ItemSchema'''
        item = Connector.create_from_type(data.item_type)
        modifiers = [Connector.instantiate_modifier(m) for m in data.modifiers]
        modifiers.append(Connector.create_from_type(data.material_type))
        # Set modifiers on the item
        for mod in modifiers:
            if mod is None: continue
            mod.apply_to(item)
        # Set the attributes if there are any
        if data.item_attributes is not None and len(data.item_attributes) > 0:
            for pattr in data.item_attributes:
                setattr(item, pattr, data.item_attributes[pattr])
        return item

    def instantiate_modifier(data):
        modifier = Connector.create_from_type(data.modifier_type)
        modifier.level = data.level
        if data.attributes is not None and len(data.attributes) > 0:
            for pattr in data.attributes:
                setattr(modifier, pattr, data.attributes[pattr])
        modifier.is_set = True
        return modifier

    def create_from_type(item_type, args=None):
        if not item_type:
            return None
        prelim_type = item_type.split('.')
        if not args: args = {}
        return getattr(
                __import__(item_type, fromlist=[prelim_type[-1]]),\
                prelim_type[-1])(**args)

    def add_player(self, playernode_object):
        '''
        Translate a PlayerNode into a Player Schema object and add it
        Used when adding a new playernode
        '''
        self.add(playernode_object, Player)

    def add_character(self, uid, lifeform_object):
        '''Used when adding a Lifeform to the database'''
        schema_id = self.get(Player, {'uid': uid}).first().id

        inv_generator = Connector.generate_inventory(lifeform_object)
        inventory = Connector.gen_to_dict(inv_generator)
        equipment = list(Connector.generate_equipped_items(lifeform_object, inventory))

        effects = list(Connector.generate_effects(lifeform_object))
        words = list(Connector.generate_words(lifeform_object))
        skills = list(Connector.generate_skills(lifeform_object))

        supplementary_data = {
            'player_id': schema_id,
            'inventory': list(inventory.values()), 
            'equipment': equipment, 
            'spell_words': words,
            'effects': effects,
            'skills': skills,
        }
        self.add(lifeform_object, Character, supplementary_data)

    def add_creature(lifeform_object):
        inv_generator = Connector.generate_inventory(lifeform_object)
        inventory = Connector.gen_to_dict(inv_generator)
        equipment = list(Connector.generate_equipped_items(lifeform_object, inventory))

        effects = list(Connector.generate_effects(lifeform_object))
        skills = list(Connector.generate_skills(lifeform_object))

        supplementary_data = {
            'inventory': list(inventory.values()), 
            'equipment': equipment, 
            'effects': effects,
            'template': lifeform_object.__module__,
            'skills': skills,
        }
        self.add(lifeform_object, Creature, supplementary_data)

    def update_character(self, character):
        '''Takes a dirty character and updates it in the database'''
        if not hasattr(character, 'uid'): return
        schema = self.get_lifeform_schema(character)
        if schema is None: return

        self.map_lifeform_to_schema(character, schema)

        self.session.add(schema)
        self.session.commit()

    def schema_params(self, obj, schema_type):
        '''Used to map to and from object to schema type'''
        obj_params = schema_type.__dict__
        for x in obj_params:
            if isinstance(obj_params[x],InstrumentedAttribute) and hasattr(obj, x):
                yield (x, getattr(obj,x))

    def generate_words(lifeform):
        '''Used to generate DB-representations of Words'''
        for word in lifeform.spell_words:
            yield Connector.create_spellword_schema(word)

    def generate_inventory(lifeform):
        '''Create Item Schema objects from a lifeform's inventory'''
        for item in lifeform.inventory:
            if item.Persistent:
                yield (item, Connector.create_inventory_schema(item))

    def generate_effects(lifeform):
        for eff in lifeform.conditions:
            if eff.Persistent:
                yield Connector.create_effect_schema(eff)

    def generate_equipped_items(character, inventory):
        '''Generator which matches the Inventory IDs against equipped slots'''
        for equip_slot in erukar.engine.lifeforms.Lifeform.equipment_types:
            equipped_item = getattr(character, equip_slot)
            if equipped_item in inventory:
                yield Connector.create_equippeditem_schema(equip_slot, inventory[equipped_item])

    def generate_skills(lifeform):
        for skill in lifeform.skills:
            yield Connector.create_skill_schema(skill)

    def create_spellword_schema(word):
        return erukar.data.Schema.SpellWord(\
                word_class=word.word_class,\
                successes = word.successes,\
                total = word.total)

    def create_inventory_schema(item):
        '''Create an Inventory Item Schema using an instance of an Item'''
        modifiers = [Connector.create_modifier_schema(m) for m in item.modifiers if m.persistent]
        item_attributes = item.persistable_attributes()
        material_module = '' if not item.material else item.material.__module__
        return erukar.data.Schema.Item(\
                item_type = item.__module__,\
                material_type = material_module,\
                modifiers = modifiers,\
                item_attributes = item_attributes)

    def create_modifier_schema(mod):
        '''create a schema from a modifier instance'''
        return erukar.data.Schema.Modifier(\
                modifier_type=mod.__module__,\
                attributes=mod.persistable_attributes(),\
                level=mod.level)

    def create_effect_schema(eff):
        return erukar.data.Schema.Effect(\
                effect_type=eff.__module__)
        
    def create_equippeditem_schema(equip_slot, item):
        return erukar.data.Schema.EquippedItem(\
                equipment_slot=equip_slot,\
                item=item)

    def create_skill_schema(skill):
        return erukar.data.Schema.Skill(\
                skill_type = skill.__module__,\
                level = skill.level,\
                attributes = skill.persistible_attributes())

    def gen_to_dict(generator):
        '''Helper which creates a dict from a generator'''
        return {x[0]:x[1] for x in generator}

