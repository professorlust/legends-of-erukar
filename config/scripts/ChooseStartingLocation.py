from erukar.server.ScriptHelpers import *

def run_script(payload): 
    payload.playernode.set_script_entry_point('handle_starting_choice')
    show_options(payload)

def show_options(payload):
    choices = payload.shard.StartingOptions
    append(payload, 'Where in the world would you like your character to start?\n')
    append(payload, '\n'.join(['{:3}: {}'.format(1+index, get_dungeon_name(choice)) for index, choice in enumerate(choices)]))

    append(payload, '\nUse the following commands to select or get more information')
    append(payload, '  {:15} -- {}'.format('#', 'Choose the location at # and begin playing'))
    append(payload, '  {:15} -- {}'.format('more about #', 'See more information about the location at #'))

def get_dungeon_name(choice):
    dungeon = __import__(choice).dungeon
    return '{1} ({0})'.format(dungeon.region, dungeon.name)

def handle_starting_choice(payload):
    if hasattr(payload, 'user_input'):
        if payload.user_input.strip().isnumeric():
            select_choice(payload)
            return
        if 'more about' in payload.user_input:
            more_about(payload)

    show_options(payload)

def select_choice(payload):
    matched_item = get_matched_item_in_list(payload.user_input, payload.shard.StartingOptions)
    if not matched_item:
        show_options(payload)
        return

    # Load in here!
    payload.playernode.character.instance = matched_item
    do_exit(payload)

def more_about(payload):
    matched_item = get_matched_item_in_list(payload.user_input, payload.shard.StartingOptions)
    dungeon = __import__(matched_item).dungeon
    append(payload, '{:10}: {}'.format('Name', dungeon.name))
    append(payload, '{:10}: {}\n'.format('Sovereignty', dungeon.sovereignty))
    append(payload, '{:10}: {}\n'.format('Region', dungeon.region))
    append(payload, dungeon.description)
    append(payload, '-'*32)

def do_exit(payload):
    payload.playernode.script_data.clear()
    payload.playernode.exit_script()
