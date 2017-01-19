import os, sys
sys.path.append(os.getcwd())

from erukar import *
import erukar

def run_script(payload):
    payload.interface.append_result(payload.uid, '-'*32)
    payload.interface.append_result(payload.uid, 'Welcome to\nLEGENDS OF ERUKAR')
    payload.interface.append_result(payload.uid, '-'*32)
