import os, sys, re
sys.path.append(os.getcwd())

from erukar import *
from erukar.server.ScriptHelpers import *
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
        ('Use Pre-Generated Character Template', switch_to_template_select), 
        ('Customize Character', switch_to_new_character),
    ]
    if exec_ui_choice(payload, choices): return

    append(payload, '\nChoose your selection via a number 1 through {}'.format(len(choices)))
    append(payload, '\n'.join('  {:2} -- {}'.format(i+1, x[0]) for i, x in enumerate(choices)))

    payload.playernode.set_script_entry_point('choose_pregen_or_custom')

def switch_to_template_select(payload):
    payload.playernode.switch_script('TemplateSelection', payload)

def switch_to_new_character(payload):
    payload.playernode.switch_script('CreateNewCharacter', payload)
