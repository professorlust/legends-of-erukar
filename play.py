from erukar import *
import readline
import numpy as np

print('This example shows the Dungeon Procedural generation')

w = Shard()
w.activate()

# Controlled Character
character = Player()
character.uid = 'a-uid'
player = PlayerNode(character.uid, character)

# Uncontrolled Character
ucharacter = Player()
ucharacter.uid = 'NonPlayableCharacter'
npc = PlayerNode(ucharacter.uid, ucharacter)

w.subscribe(player)
w.subscribe(npc)
w.interface.execute(character.uid, 'join')
#w.interface.execute(npc.uid, 'join')

while True:
    print('-' * 64)
    line = input('')
    res = w.interface.execute(player.character.uid, line)
