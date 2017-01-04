import os, sys
sys.path.append(os.getcwd())

from erukar import *
import erukar

def run_script(payload):
    payload.interface.append_result(payload.uid, 'Welcome to\nLEGENDS OF ERUKAR\n')
