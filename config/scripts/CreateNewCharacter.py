import os, sys, re

from erukar.server.ScriptHelpers import *
from erukar import *
import erukar

def run_script(payload):
    handle_stat_allocation(payload)

def return_to_previous(payload):
    payload.playernode.switch_script('CharacterCreation', payload)

def handle_stat_allocation(payload):
    payload.playernode.set_script_entry_point('handle_stat_allocation')
    payload.playernode.character.wealth = payload.shard.StartingWealth
    payload.playernode.inventory = []

    stats = ['strength','dexterity','vitality','acuity','sense','resolve']

    if hasattr(payload, 'user_input'):
        if 'continue' in payload.user_input:
            append(payload, 'Your stat allocation is now locked. You can level up in game through the \'level\' command.')
            handle_skill_allocation(payload)
            return

        if 'back' in payload.user_input:
            return_to_previous(payload)
            return

        try:
            a_or_r, amount, stat = re.search('(add|remove)\s+(\d+)\s+(?:to|from)\s+(\w+)', payload.user_input).groups()
        except:
            append(payload, 'Could not parse that input. Try again!')
            return

        stats = ['strength','dexterity','vitality','acuity','sense','resolve']
        stat_var_name = get_closest_match(stat, stats)
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


def show_stat_allocation_display(payload):
    append(payload, '\nYou have {} points to allocate between your stats.\n'.format(payload.character.stat_points))
    stat_results = '\n'.join(Stats.stat_descriptions(payload.character))
    append(payload, stat_results)
    append(payload, '\nPlease use the following commands to create your character')
    append(payload, '  {:15} -- {}'.format('add X to Y', 'Add X points to Y stat'))
    append(payload, '  {:15} -- {}'.format('remove X from Y', 'Remove X points from Y stat'))
    append(payload, '  {:15} -- {}'.format('back', 'Exit stat distribution and return to previous menu'))
    append(payload, '  {:15} -- {}'.format('continue', 'Exit stat distribution and continue to skill allocation\n'))


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


def do_exit(payload):
    payload.playernode.character.define_level(1)
    payload.playernode.script_data.clear()
    payload.playernode.switch_script('ChooseStartingLocation', payload)

