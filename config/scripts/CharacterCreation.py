import os, sys, re
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
    payload.playernode.character.wealth = 250
    payload.playernode.inventory = []

    if hasattr(payload, 'user_input'):
        if 'exit' in payload.user_input:
            append(payload, 'Your stat allocation is now locked. You can level up in game through the \'level\' command.')
            handle_skill_allocation(payload)
            return

        try:
            a_or_r, amount, stat = re.search('(add|remove)\s+(\d+)\s+(?:to|from)\s+(\w+)', payload.user_input).groups()
        except:
            append(payload, 'Could not parse that input. Try again!')
            return
        stat_var_name = decode_stat(stat)
        cur_val = getattr(payload.playernode.character, stat_var_name)

        if a_or_r == 'add':
            if int(amount) > payload.playernode.character.stat_points:
                append(payload, 'Truncating to {pts}, as you only have {pts} to spend.'.format(pts=payload.playernode.character.stat_points))
                amount = payload.playernode.character.stat_points
            setattr(payload.playernode.character, stat_var_name, cur_val + int(amount))
            payload.playernode.character.stat_points -= int(amount)
            append(payload, 'Adding {} to {}'.format(int(amount), stat_var_name))

        if a_or_r == 'remove':
            new_level = max(0, cur_val - int(amount))
            payload.playernode.character.stat_points += cur_val - new_level
            setattr(payload.playernode.character, stat_var_name, new_level)
            append(payload, 'removing {} from {}'.format(amount, stat_var_name))

    show_stat_allocation_display(payload)

def decode_stat(stat_string):
    stats = ['strength','dexterity','vitality','acuity','sense','resolve']
    if len(stat_string) < 2: 
        return stats[0]
    return next(x for x in stats if stat_string.lower() in x.lower()) 

def handle_skill_allocation(payload):
    append(payload, '\nThis is where you will pick skills\n')
    handle_inventory(payload)

def handle_inventory(payload):
    shop = make_shop(payload)
    append(payload, 'Please pick your default inventory. You have {} riphons to spend.\n'.format(payload.playernode.character.wealth))
    append(payload, '\n'.join(shop.display_inventory()))
    append(payload, '\nUse the following commands to buy or sell items\n')
    append(payload, '  {:15} -- {}'.format('buy #', 'Buy item at seller\'s # (if you can afford it)'))
    append(payload, '  {:15} -- {}'.format('my items', 'See items in your inventory'))
    append(payload, '  {:15} -- {}'.format('sell my #', 'Buy sell item at your #'))
    append(payload, '  {:15} -- {}'.format('more about #', 'See detailed information about seller\'s item at #'))
    append(payload, '  {:15} -- {}'.format('more about my #', 'See detailed information about your item at #'))
    append(payload, '  {:15} -- {}'.format('back', 'Return to previous menu'))
    append(payload, '  {:15} -- {}'.format('exit', 'Commit and exit inventory management\n'))

def interpret_inventory_response(payload):
    shop = make_shop(payload)
    if not hasattr(payload, 'user_input'):
        handle_inventory(payload)
        return

    if 'my' in payload.user_input:
        handle_a_my_inventory_command(payload)
        return

    if 'back' in payload.user_input:
        choose_pregen_or_custom(payload)
        return

    if 'exit' in payload.user_input:
        do_exit(payload)
        return

    matched_item = get_matched_item_in_list(payload.user_input, shop.inventory)
    if not matched_item: return

    if 'buy' in payload.user_input:
        result = shop.sell_to_buyer(matched_item, payload.playernode.character)
        append(payload, result)
        handle_inventory(payload)
        return

    if 'more about' in payload.user_input:
        append(payload, matched_item.on_inventory_inspect(payload.playernode.character))


def handle_a_my_inventory_command(payload):
    ui = payload.user_input
    shop = make_shop(payload)

    if 'items' in ui:
        inventory = ['{:3} -- {}'.format(i+1, item.format()) for i, item in enumerate(payload.playernode.character.inventory)]
        append(payload, '\n'.join(inventory))
        return

    matched_item = get_matched_item_in_list(payload.user_input, payload.playernode.character.inventory)
    if not matched_item: return

    if 'sell' in ui:
        result = shop.buy_from_seller(matched_item, payload.playernode.character)
        append(payload, result)
        return

    if 'more about' in ui:
        append(payload, matched_item.on_inventory_inspect(payload.playernode.character))

def match_first_digit(ui):
    match = re.search('\s+(\d+)', ui)
    if match:
        return int(match.group(1))-1
    return -1

def get_matched_item_in_list(ui, matchlist):
    index = match_first_digit(ui)
    if 0 <= index < len(matchlist):
        return matchlist[index]

def make_shop(payload):
    '''Either makes a new shop or retrieves the one established in script_data'''
    # Check to see if we already have a shop in the script_data
    if 'character_creation_shop' in payload.playernode.script_data:
        return payload.playernode.script_data['character_creation_shop']
    # No? gotta create one then
    shop = Shop(500)
    shop.has_infinite_supply = True
    payload.playernode.set_script_entry_point('interpret_inventory_response')
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
    cleric.sense     = 5
    cleric.resolve   = 2
    
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
    append(payload, '\nClerics can cast a healing spell, a blessing, and can use holy water to purify a room from evil.')

    append(payload, '\nChoose Cleric?')
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('define_cleric')

def choose_cleric(payload):
    perform_template_choice(payload, 'cleric')
    
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
    
    fighter.define_level(1)
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
    
    mage.define_level(1)
    mage.inventory = [
        Shop.create(Wand, erukar.game.modifiers.material.Oak),
        Candle(),
        Shop.create(Robes, erukar.game.modifiers.material.Cotton),
        Shop.create(Sandals, erukar.game.modifiers.material.Leather),
        Shop.create(Breeches, erukar.game.modifiers.material.Cotton),
        Potion(5)
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
    
    ranger.define_level(1)
    ranger.inventory = [
        Shop.create(Bow, erukar.game.modifiers.material.Oak),
        Shop.create(Boots, erukar.game.modifiers.material.Leather),
        Shop.create(Vest, erukar.game.modifiers.material.Leather),
        Shop.create(Breeches, erukar.game.modifiers.material.Leather),
        Potion(5) # This should be replaced with ammo
    ]
    ranger.right = ranger.inventory[0]
    ranger.feet  = ranger.inventory[1]
    ranger.chest = ranger.inventory[2]
    ranger.legs  = ranger.inventory[3]
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
