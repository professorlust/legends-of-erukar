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
    handle_stat_allocation(payload)

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
    shop = Shop(50)
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

    append(payload, 'Please pick your default inventory. You have {} riphons to spend.'.format(50))
    append(payload, '\n'.join(shop.display_inventory()))

def show_stat_allocation_display(payload):
    append(payload, 'You have {} points to allocate between your stats.'.format(payload.character.stat_points))
    stat_results = '\n'.join(Stats.stat_descriptions(payload.character))
    append(payload, stat_results)
    append(payload, '\nPlease use the following commands to create your character')
    append(payload, '  {:15} -- {}'.format('add X to Y', 'Add X points to Y stat'))
    append(payload, '  {:15} -- {}'.format('remove X from Y', 'Remove X points from Y stat'))
    append(payload, '  {:15} -- {}'.format('exit', 'Commit and exit stat distribution\n'))

def append(payload, string):
    payload.interface.append_result(payload.uid, string)
