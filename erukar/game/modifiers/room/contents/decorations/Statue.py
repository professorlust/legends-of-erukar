from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random, collections

class Statue(RoomModifier):
    Probability = 1
    materials = [
        "marble",
        "granite",
        "copper",
        "brass",
        "iron"
    ]
    conditions = [
        "This statue appears to be incomplete, as if the artist had just recently been working on it and taken a short break.",
        "The statue looks like it has almost been finished, but is relatively unpolished.",
        "The statue is freshly complete and in good condition.",
        "The statue seems to have sustained some sort of damage from a weapon of some sort.",
        "Time has not been kind to this statue. It is covered in scratches and even some cracks.",
        "The statue is in terrible disorder. It is missing several key features and its subject matter is almost indiscriminable."
    ]
    topics = [
        "the Hero {m_name} of {tribe}",
        "the Heroine {f_name} of {tribe}",
        "the King of {tribe}, {m_name}",
        "the Queen of {tribe}, {f_name}",
        "{m_name}, God of {domain}",
        "{1}, Goddess of {domain}"
    ]
    m_names = [
        "Ilewer",
        "Molataire",
        "Gyle",
        "Rion",
        "Wethyr",
        "Ajamal",
        "Ardor",
        "Alabir",
        "Garlen",
        "Iorchel",
        "Kith"
    ]
    f_names = [
        "Ophrea",
        "Aorda",
        "Bertre",
        "Lirona",
        "Raphia",
        "Mode",
        "Nabione"
    ]
    tribes = [
        "Erukar",
        "Orukar",
        "Velmyre",
        "Iuria",
        "Valoris",
        "Zygest",
        "Thylos",
        "The Kholte Commonwealth",
        "Lorthenia",
        "the Thaedoth Theocracy"
    ]
    domains = [
        "fire",
        "water",
        "wind",
        "earth",
        "creation",
        "damnation",
        "acid",
        "sound",
        "poison",
        "death",
        "life"
    ]
    broad_alias_base="{material} statue"
    broad_result_base="There is a {material} statue to the {location} of the room."
    inspect_result_base="This is a {material} statue depicting {topic}. {condition}"

    def randomize(self):
        self.material = random.choice(Statue.materials)
        self.condition = random.choice(Statue.conditions)
        self.m_name = random.choice(Statue.m_names)
        self.f_name = random.choice(Statue.f_names)
        self.tribe = random.choice(Statue.tribes)
        self.topic = random.choice(Statue.topics)
        self.domain = random.choice(Statue.domains)

    def __init__(self):
        self.randomize()

    def get_arguments(self, location):
        return { 'material': self.material,
                'condition': self.condition,
                'm_name': self.m_name,
                'f_name': self.f_name,
                'tribe': self.tribe,
                'topic': self.topic,
                'location': location,
                'domain': self.domain }

    def apply_to(self, room):
        try:
            location = random.choice(list(room.wall_directions())).name
        except:
            location = 'center'
        arguments = self.get_arguments(location)
        deco = Decoration(aliases=[Statue.broad_alias_base.format(**arguments)],
            broad_results = Statue.broad_result_base.format(**arguments).format(**arguments),
            inspect_results=Statue.inspect_result_base.format(**arguments).format(**arguments))
        room.add(deco)
