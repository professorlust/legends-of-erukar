from erukar import *
from examples.helpers.ExampleRunner import ExampleRunner
import numpy as np

print('This example shows the Dungeon Procedural generation')

d = DungeonManager()
gen_params = GenerationProfile(*(np.random.uniform(-1, 1) for x in range(4)))
d.activate(gen_params)

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

# Needs to be added to GameManager
interface = Interface()
interface.data.players.append(player)
interface.data.players.append(npc)
d.subscribe(player)
d.subscribe(npc)
print(interface.execute(character.uid, 'inspect'))

while True:
    turn = d.turn_manager.next()
    print('It is now {0}\'s turn\n'.format(turn.uid))
    if turn is player:
        line = input('> ')
        print('-' * 64)
        res = interface.execute(turn.character.uid, line)
        if res is not None:
            print(res)
