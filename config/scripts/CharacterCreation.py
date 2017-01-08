import os, sys
sys.path.append(os.getcwd())

from erukar import *
import erukar

def run_script(payload):
    append(payload, 'Before you begin, you must create a character.')
    append(payload, 'What is your name?')
    payload.playernode.set_script_entry_point('set_name')

def set_name(payload):
    payload.character.name = payload.user_input 
    append(payload, 'Your character\'s name is now {}!'.format(payload.character.name))
    del payload.user_input
    choose_pregen_or_custom(payload)

def choose_pregen_or_custom(payload):
    choices = [
        ('Use Pre-Generated Character Template', select_template), 
        ('Customize Character', handle_stat_allocation),
    ]
    if exec_ui_choice(payload, choices): return

    append(payload, '\nChoose your selection via a number 1 through {}'.format(len(choices)))
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('choose_pregen_or_custom')

def select_template(payload):
    choices = [
        ('Barbarian', define_barbarian), 
        ('Cleric', define_cleric),
        ('Fighter', define_fighter),
        ('Mage', define_mage),
        ('Ranger', define_ranger),
        ('Previous Menu', choose_pregen_or_custom)
    ]
    if exec_ui_choice(payload, choices): return

    append(payload, '\nChoose your template via a number 1 through {}'.format(len(choices)))
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('select_template')


def handle_stat_allocation(payload):
    payload.playernode.set_script_entry_point('handle_stat_allocation')
    if hasattr(payload, 'user_input'):
        if payload.user_input.strip() == 'exit':
            append(payload, 'Your stat allocation is now locked. You can level up in game through the \'level\' command.')
            handle_skill_allocation(payload)
            return
        append(payload, 'Unrecognized command.')
        
    show_stat_allocation_display(payload)

def handle_skill_allocation(payload):
    append(payload, '\nThis is where you will pick skills\n')
    handle_inventory(payload)

def handle_inventory(payload):
    shop = make_shop(payload)
    append(payload, 'Please pick your default inventory. You have {} riphons to spend.'.format(50))
    append(payload, '\n'.join(shop.display_inventory()))
    append(payload, '\nUse the following commands to buy or sell items\n')
    append(payload, '  {:15} -- {}'.format('buy #', 'Buy item at seller\'s # (if you can afford it)'))
    append(payload, '  {:15} -- {}'.format('my items', 'See items in your inventory'))
    append(payload, '  {:15} -- {}'.format('sell my #', 'Buy sell item at your #'))
    append(payload, '  {:15} -- {}'.format('more about #', 'See detailed information about seller\'s item at #'))
    append(payload, '  {:15} -- {}'.format('more about my #', 'See detailed information about your item at #'))
    append(payload, '  {:15} -- {}'.format('exit', 'Commit and exit inventory management\n'))

def make_shop(payload):
    '''Either makes a new shop or retrieves the one established in script_data'''
    # Check to see if we already have a shop in the script_data
    if 'character_creation_shop' in payload.playernode.script_data:
        append(payload, 'Retrieved a shop')
        return payload.playernode.script_data['character_creation_shop']
    # No? gotta create one then
    shop = Shop(50)
    payload.playernode.set_script_entry_point('handle_inventory')
    # Add Inventory
    for item in [Axe, Sword, CrossBow, Buckler, RoundShield, Cuirass, Guard, Greaves]:
        for material in [erukar.game.modifiers.material.Iron, erukar.game.modifiers.material.Steel]:
            shop.inventory.append(Shop.create(item, material))
    for item in [Staff, Bow]:
        for material in [erukar.game.modifiers.material.Ash, erukar.game.modifiers.material.Iurwood, erukar.game.modifiers.material.Oak]:
            shop.inventory.append(Shop.create(item, material))
    for item in [Boots, Sandals, Treads]:
        shop.inventory.append(Shop.create(item, erukar.game.modifiers.material.Leather))
    for item in [Robes, Tunic, Breeches]:
        for material in [erukar.game.modifiers.material.Cotton, erukar.game.modifiers.material.Silk]:
            shop.inventory.append(Shop.create(item, material))
    shop.inventory.append(Potion())
    shop.inventory.append(Torch())
    shop.inventory.append(Candle())
    shop.inventory.append(erukar.game.inventory.consumables.keys.IronKey())
    shop.inventory.append(erukar.game.inventory.consumables.keys.SteelKey())
    # Save into script_data
    payload.playernode.script_data['character_creation_shop'] = shop
    return shop

def show_stat_allocation_display(payload):
    append(payload, 'You have {} points to allocate between your stats.'.format(payload.character.stat_points))
    stat_results = '\n'.join(Stats.stat_descriptions(payload.character))
    append(payload, stat_results)
    append(payload, '\nPlease use the following commands to create your character')
    append(payload, '  {:15} -- {}'.format('add X to Y', 'Add X points to Y stat'))
    append(payload, '  {:15} -- {}'.format('remove X from Y', 'Remove X points from Y stat'))
    append(payload, '  {:15} -- {}'.format('exit', 'Commit and exit stat distribution\n'))

'''Template Creation'''
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
    
    barbarian.define_level(1)
    barbarian.inventory = [
        Shop.create(Axe, erukar.game.modifiers.material.Iron),
        Shop.create(Mace, erukar.game.modifiers.material.Iurwood),
        Shop.create(Breeches, erukar.game.modifiers.material.Leather),
        Candle(),
    ]

    barbarian.left  = barbarian.inventory[0]
    barbarian.right = barbarian.inventory[1]
    barbarian.legs  = barbarian.inventory[2]
    barbarian.currency = 50 - sum(i.price() for i in barbarian.inventory)
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

def make_cleric(payload):
    if 'cleric' in payload.playernode.script_data:
        append(payload, 'Retrieved a cleric')
        return payload.playernode.script_data['cleric']
    cleric = Player()
    cleric.strength  = 3
    cleric.dexterity = 1
    cleric.vitality  = 3
    cleric.acuity    = 1
    cleric.sense     = 3
    cleric.resolve   = 4
    
    cleric.define_level(1)
    cleric.inventory = [
        Shop.create(Mace, erukar.game.modifiers.material.Iron),
        Shop.create(Piece, erukar.game.modifiers.material.Chainmail),
        Shop.create(Leggings, erukar.game.modifiers.material.Chainmail),
        Shop.create(Treads, erukar.game.modifiers.material.Leather),
        Potion(5),
    ]
    cleric.left  = cleric.inventory[0]
    cleric.chest = cleric.inventory[1]
    cleric.legs  = cleric.inventory[2]
    cleric.feet  = cleric.inventory[3]
    cleric.currency = 50 - sum(i.price() for i in cleric.inventory)
    payload.playernode.script_data['cleric'] = cleric
    return cleric

def define_cleric(payload):
    choices = [
        ('Yes', choose_cleric),
        ('No', select_template),
    ]
    if exec_ui_choice(payload, choices): return

    cleric = make_cleric(payload)

    append(payload, 'Clerics are holy warriors who specialize in purification and sanctification. Clerics use a weapon of their choice and a holy symbol, which provides bonuses while within hallowed areas.')
    append(payload, 'Base Stats\n----------')
    append(payload, '\n'.join(Stats.stat_descriptions(cleric, show_raw=True)))
    append(payload, '\nInventory\n----------')
    append(payload, '\n'.join(Inventory.inventory_contents(cleric)))
    append(payload, '\nClerics can cast a healing spell, a blessing, and can use holy water to purify a room from evil.')

    append(payload, '\nChoose Cleric?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_cleric')


def choose_cleric(payload):
    perform_template_choice(payload, 'cleric')
    
def define_fighter(payload):
    pass

def make_fighter(payload):
    perform_template_choice(payload, 'fighter')

def define_mage(payload):
    pass

def make_mage(payload):
    perform_template_choice(payload, 'mage')

def define_ranger(payload):
    pass

def make_ranger(payload):
    perform_template_choice(payload, 'ranger')

'''Helper Methods'''
def perform_template_choice(payload, template_name):
    append(payload, 'You are entering the game as a {}!'.format(template_name.capitalize()))

    payload.playernode.character = payload.playernode.script_data[template_name.lower()]
    payload.playernode.script_data.clear()

    payload.playernode.exit_script()

def append(payload, string):
    payload.interface.append_result(payload.uid, string)

def exec_ui_choice(payload, choices):
    '''Attempts to call a method based on the payload's user input'''
    if hasattr(payload, 'user_input'):
        ui = payload.user_input
        del payload.user_input
        if ui.isnumeric() and 0 <= int(ui)-1 < len(choices):
            choices[int(ui)-1][1](payload) 
            return True
    return False
