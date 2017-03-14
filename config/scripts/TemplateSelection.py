from erukar.server.ScriptHelpers import *
from erukar.engine.magic.SpellWordGrasp import SpellWordGrasp
from erukar import *
import erukar

def run_script(payload):
    select_template(payload)

def return_to_previous(payload):
    payload.playernode.switch_script('CharacterSelect', payload)

def select_template(payload):
    choices = [
        ('Barbarian', define_barbarian), 
        ('Cleric', define_cleric),
        ('Fighter', define_fighter),
        ('Mage', define_mage),
        ('Ranger', define_ranger),
        ('Previous Menu', return_to_previous)
    ]
    if exec_ui_choice(payload, choices): return

    append(payload, '\nChoose your template via a number 1 through {}'.format(len(choices)))
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('select_template')


'''Barbarian'''
def make_barbarian(payload):
    if 'barbarian' in payload.playernode.script_data:
        append(payload, 'Retrieved a barbarian')
        return payload.playernode.script_data['barbarian']
    barbarian = Player()
    barbarian.strength  = 4
    barbarian.dexterity = 1
    barbarian.vitality  = 4
    barbarian.acuity    = 1
    barbarian.sense     = 1
    barbarian.resolve   = 4
    
    barbarian.inventory = [
        Shop.create(Axe, erukar.game.modifiers.material.Iron),
        Shop.create(Mace, erukar.game.modifiers.material.Iurwood),
        Shop.create(Breeches, erukar.game.modifiers.material.Leather),
        Candle(),
    ]

    barbarian.left  = barbarian.inventory[0]
    barbarian.right = barbarian.inventory[1]
    barbarian.legs  = barbarian.inventory[2]

    barbarian.spell_words = [
        SpellWordGrasp('InflictCondition', 1, 1),
        SpellWordGrasp('Enraged', 1, 1)
    ]
    payload.playernode.script_data['barbarian'] = barbarian
    return barbarian

def define_barbarian(payload):
    choices = [
        ('Yes', choose_barbarian),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    barbarian = make_barbarian(payload)

    append(payload, 'Barbarians are hardy melee fighters capable of dealing lots of damage in bursts. Their raw strength allows them great amounts of damage with heavy, blunted weapons such as Maces and Staves.\n')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(barbarian, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(barbarian)))
    append(payload, '\nEach barbarian has access to a skill called "Rage" which temporarily grants bonuses to attack damage/health equal to the barbarian\'s resolve score and a 33% increase to physical damage mitigation.')

    append(payload, '\nChoose Barbarian?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_barbarian')

def choose_barbarian(payload):
    perform_template_choice(payload, 'barbarian')


'''Cleric'''
def make_cleric(payload):
    if 'cleric' in payload.playernode.script_data:
        append(payload, 'Retrieved a cleric')
        return payload.playernode.script_data['cleric']
    cleric = Player()
    cleric.strength  = 3
    cleric.dexterity = 1
    cleric.vitality  = 3
    cleric.acuity    = 1
    cleric.sense     = 5
    cleric.resolve   = 2
    
    cleric.inventory = [
        Shop.create(Mace, erukar.game.modifiers.material.Iron),
        Shop.create(Piece, erukar.game.modifiers.material.Chainmail),
        Shop.create(Leggings, erukar.game.modifiers.material.Chainmail),
        Shop.create(Treads, erukar.game.modifiers.material.Leather),
        Potion(5),
    ]
    cleric.spell_words = [
        SpellWordGrasp('Consecrate', 1, 1),
        SpellWordGrasp('HealEffect', 1, 1),
        SpellWordGrasp('Persistent', 1, 1),
    ]

    cleric.left  = cleric.inventory[0]
    cleric.chest = cleric.inventory[1]
    cleric.legs  = cleric.inventory[2]
    cleric.feet  = cleric.inventory[3]
    payload.playernode.script_data['cleric'] = cleric
    return cleric

def define_cleric(payload):
    choices = [
        ('Yes', choose_cleric),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    cleric = make_cleric(payload)

    append(payload, 'Clerics are holy warriors who specialize in purification and sanctification. Clerics use a weapon of their choice and a holy symbol, which provides bonuses while within hallowed areas. They have a strong sense score which allows them to sense otherworldly presences.')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(cleric, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(cleric)))
    append(payload, '\nClerics can use holy water or a consecration spell word to purify a room from evil. They also have access to a word which heals and one which persists effects for a duration of time.')

    append(payload, '\nChoose Cleric?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_cleric')

def choose_cleric(payload):
    perform_template_choice(payload, 'cleric')
    

'''Fighter'''
def make_fighter(payload):
    if 'fighter' in payload.playernode.script_data:
        append(payload, 'Retrieved a fighter')
        return payload.playernode.script_data['fighter']
    fighter = Player()
    fighter.strength  = 5
    fighter.dexterity = 2
    fighter.vitality  = 5
    fighter.acuity    = 1
    fighter.sense     = 1
    fighter.resolve   = 1
    
    fighter.inventory = [
        Shop.create(Sword, erukar.game.modifiers.material.Iron),
        Shop.create(HeaterShield, erukar.game.modifiers.material.Oak),
        Shop.create(Piece, erukar.game.modifiers.material.Chainmail),
        Shop.create(Leggings, erukar.game.modifiers.material.Chainmail),
        Shop.create(Treads, erukar.game.modifiers.material.Leather),
        Shop.create(Spear, erukar.game.modifiers.material.Iron),
    ]
    fighter.right = fighter.inventory[0]
    fighter.left  = fighter.inventory[1]
    fighter.chest = fighter.inventory[2]
    fighter.legs  = fighter.inventory[3]
    fighter.feet  = fighter.inventory[4]
    payload.playernode.script_data['fighter'] = fighter
    return fighter

def define_fighter(payload):
    choices = [
        ('Yes', choose_fighter),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    fighter = make_fighter(payload)

    append(payload, 'Fighters are skilled in hand to hand combat. They specialize in advanced combat maneuvers and tightly controlled attacks which minimize opportunities for counterattacks.')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(fighter, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(fighter)))
    append(payload, '\nFighters start with no active spells but have advanced training in parrying, swords, spears, and shields.')

    append(payload, '\nChoose Fighter?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_fighter')

def choose_fighter(payload):
    perform_template_choice(payload, 'fighter')


'''Mage'''
def make_mage(payload):
    if 'mage' in payload.playernode.script_data:
        append(payload, 'Retrieved a mage')
        return payload.playernode.script_data['mage']
    mage = Player()
    mage.strength  = 1
    mage.dexterity = 2
    mage.vitality  = 1
    mage.acuity    = 6
    mage.sense     = 2
    mage.resolve   = 2
    
    mage.inventory = [
        Shop.create(Wand, erukar.game.modifiers.material.Oak),
        Candle(),
        Shop.create(Robes, erukar.game.modifiers.material.Cotton),
        Shop.create(Sandals, erukar.game.modifiers.material.Leather),
        Shop.create(Breeches, erukar.game.modifiers.material.Cotton),
        Potion(5)
    ]
    mage.spell_words = [
        SpellWordGrasp('Fire', 1, 1),
        SpellWordGrasp('Ice', 1, 1),
        SpellWordGrasp('Electricity', 1, 1),
        SpellWordGrasp('Barrier', 1, 1),
        SpellWordGrasp('Bolt', 1, 1),
        SpellWordGrasp('DamageSingleTarget', 1, 1),
        SpellWordGrasp('DamageOverTime', 1, 1),
    ]
    mage.skills = [
        erukar.engine.base.skills.ArcaneGift()
    ]
    mage.right = mage.inventory[0]
    mage.left  = mage.inventory[1]
    mage.chest = mage.inventory[2]
    mage.feet  = mage.inventory[3]
    mage.legs  = mage.inventory[4]
    payload.playernode.script_data['mage'] = mage
    return mage

def define_mage(payload):
    choices = [
        ('Yes', choose_mage),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    mage = make_mage(payload)

    append(payload, 'Mages excel in observation and intellect. Their orders are highly diverse and tend to attract the most intelligent of indivuals. Mages specialize in casting arcane magics, though some may tend to prefer alchemy or research.')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(mage, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(mage)))
    append(payload, '\nMages start with several Arcane Words: Three Elemental Augments (Ice, Fire, and Electric) and two Spellshapes (Bolt, Shield). By combining these words, they can shape their spells to their needs with minimal downtime.')

    append(payload, '\nChoose Mage?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_mage')

def choose_mage(payload):
    perform_template_choice(payload, 'mage')


'''Ranger'''
def make_ranger(payload):
    if 'ranger' in payload.playernode.script_data:
        append(payload, 'Retrieved a ranger')
        return payload.playernode.script_data['ranger']
    ranger = Player()
    ranger.strength  = 3
    ranger.dexterity = 5
    ranger.vitality  = 2
    ranger.acuity    = 2
    ranger.sense     = 2
    ranger.resolve   = 1
    
    ranger.inventory = [
        Shop.create(Bow, erukar.game.modifiers.material.Oak),
        Shop.create(Boots, erukar.game.modifiers.material.Leather),
        Shop.create(Vest, erukar.game.modifiers.material.Leather),
        Shop.create(Breeches, erukar.game.modifiers.material.Leather),
        Shop.create(Arrow, erukar.game.modifiers.material.Oak),
        Potion(5) # This should be replaced with ammo
    ]
    ranger.right = ranger.inventory[0]
    ranger.feet  = ranger.inventory[1]
    ranger.chest = ranger.inventory[2]
    ranger.legs  = ranger.inventory[3]
    ranger.ammunition = ranger.inventory[4]
    payload.playernode.script_data['ranger'] = ranger
    return ranger

def define_ranger(payload):
    choices = [
        ('Yes', choose_ranger),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    ranger = make_ranger(payload)

    append(payload, 'Rangers are marksmen, specializing in the art of archery and ranged combat. They tend to prefer keeping ther targets at a distance.')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(ranger, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(ranger)))
    append(payload, '\nRangers start with advanced training in bows and crossbows and have Snipe, an active skill which provides additional accuracy at long ranges at the cost of damage.')

    append(payload, '\nChoose Ranger?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_ranger')

def choose_ranger(payload):
    perform_template_choice(payload, 'ranger')

'''Helper Methods'''
def perform_template_choice(payload, template_name):
    append(payload, 'You are entering the game as a {}!'.format(template_name.capitalize()))

    payload.playernode.character = payload.playernode.script_data[template_name.lower()]
    payload.playernode.character.wealth = 250 - sum(x.price() for x in payload.playernode.character.inventory)

    do_exit(payload)


def do_exit(payload):
    payload.playernode.character.define_level(1)
    payload.playernode.script_data.clear()
    payload.playernode.switch_script('ChooseStartingLocation', payload)

