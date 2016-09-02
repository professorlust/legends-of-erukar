from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random, collections

class Statue(RoomModifier):
    Probability = 0.00
    materials = [
        "gypsum",
        "alabaster",
        "jade",
        "agate",
        "onyx",
        "rock crystal",
        "basalt",
        "carbonatite",
        "obsidian",
        "norite",
        "quartz",
        "ceramic",
        "marble",
        "granite",
        "copper",
        "bronze",
        "brass",
        "aluminum",
        "plaster",
        "glass",
        "iron",
        "wood"
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
        "the Hero {m_name} of {tribe}. {m_pronoun}",
        "the Heroine {f_name} of {tribe}. {f_pronoun}",
        "the King of {tribe}, {m_name}. {k_pronoun}",
        "the Queen of {tribe}, {f_name}. {q_pronoun}",
        "{god_name}, God of {domain}. {g_pronoun}"
    ]
    m_pronouns = [
        "He",
        "The hero",
        "{m_name}"
    ]
    f_pronouns = [
        "She",
        "The heroine",
        "{f_name}"
    ]
    k_pronouns = [
        "The King",
        "He",
        "King {m_name}",
        "His Majesty",
        "His Grace",
        "{m_name}"
    ]
    q_pronouns = [
        "The Queen",
        "She",
        "Queen {f_name}",
        "Her Majesty",
        "Her Grace",
        "{f_name}"
    ]
    g_pronouns = [
        "The God",
        "The God of {domain}",
        "{god_name}"
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
        "Kith",
        "Reastus",
        "Basten",
        "Kellan",
        "Alvus"
    ]
    god_names = [
        "The Vanguard",
        "The Keeper of Time",
        "The Judge",
        "The Eagle",
        "The Creator",
        "The Corruptor",
        "The Condor",
        "The Destroyer"
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
        "the Thaedoth Theocracy",
        "Maristir",
        "Alavas",
        "Arlon",
        "Falonde",
        "Edrhel",
        "Lionde",
        "Halondir",
        "Maraland",
        "Hvelithos"
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
    positions = [
        'kneeling',
        'sitting',
        'in a fetal position',
        'contrapposto',
        'in a one-legged standing position',
        'standing',
        'supine',
        'prone',
        'in a crouching position',
        'in a headstand',
        'in an aggressive stance',
        'in a defensive stance'
    ]

    fields = [ 
        'material',
        'condition',
        'god_name',
        'g_pronoun',
        'domain' ,
        'm_name',
        'm_pronoun',
        'f_name',
        'f_pronoun',
        'q_pronoun',
        'k_pronoun',
        'tribe',
        'topic',
        'position']
        
    broad_alias_base="{material} statue"
    broad_result_base="There is a {material} statue to the {location} of the room."
    inspect_result_base="This is a {material} statue depicting {topic} is {position}. {condition}"

    def get_arguments(self, location):
        all_but_loc = super().get_arguments() 
        all_but_loc['location'] = location
        return all_but_loc

    def apply_to(self, room):
        try:
            location = random.choice(list(room.wall_directions())).name
        except:
            location = 'center'
        arguments = self.get_arguments(location)
        deco = Decoration(aliases=[self.mutate(self.broad_alias_base, arguments)],
            broad_results=self.mutate(self.broad_result_base, arguments),
            inspect_results=self.mutate(self.inspect_result_base, arguments))
        room.add(deco) 
