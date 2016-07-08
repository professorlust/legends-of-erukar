from erukar import *
from examples.helpers.ExampleRunner import ExampleRunner
import numpy as np

print('This example shows the Dungeon Procedural generation')

w = GameManager()
w.activate()

# Controlled Character
character = Player()
character.uid = 'ControlledPlayer'
character.define_stats({'dexterity': 2, 'acuity': 0})
player = PlayerNode(character.uid, character)

# Uncontrolled Character
ucharacter = Player()
ucharacter.uid = 'NonPlayableCharacter'
ucharacter.define_stats({'dexterity': 2, 'acuity': 0})
npc = PlayerNode(ucharacter.uid, ucharacter)

w.subscribe(player)
w.subscribe(npc)
print(w.interface.execute(character.uid, 'inspect'))

while True:
    turn = w.dungeons[0].turn_manager.next()
    print('It is now {0}\'s turn\n'.format(turn.uid))
    if turn is player:
        line = input('> ')
        print('-' * 64)
        res = w.interface.execute(turn.character.uid, line)
        if res is not None:
            print(res)
