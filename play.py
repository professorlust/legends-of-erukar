from erukar import *
import readline
import os, sys
import numpy as np

sys.path.append(os.getcwd() + '/hubs')

print('This example shows the Dungeon Procedural generation')

w = Shard()
w.activate()

w.subscribe('a-uid')

while True:
    print('-' * 64)
    line = input('')
    res = w.interface.execute('a-uid', line)
    print(w.interface.get_messages_for('a-uid'))
