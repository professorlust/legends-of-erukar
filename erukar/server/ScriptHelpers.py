import re

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

def get_closest_match(input_str, options):
    if len(input_str) < 2: 
        return options[0]
    return next(x for x in options if input_str.lower() in x.lower()) 

def match_first_digit(ui):
    match = re.search('(\d+)', ui)
    if match:
        return int(match.group(1))-1
    return -1

def get_matched_item_in_list(ui, matchlist):
    index = match_first_digit(ui)
    if 0 <= index < len(matchlist):
        return matchlist[index]
