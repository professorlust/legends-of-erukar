from erukar import *
import readline
import os, sys
import numpy as np

sys.path.append(os.getcwd() + '/hubs')

print('This example shows the Dungeon Procedural generation')

w = Shard()
w.activate()

w.subscribe('a-uid')

w.interface.execute('a-uid', 'join')

while True:
    print('-' * 64)
    line = input('')
    res = w.interface.execute('a-uid', line)
