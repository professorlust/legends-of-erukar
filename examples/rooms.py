from erukar import *
from examples.helpers.ExampleRunner import ExampleRunner
import numpy as np

print('Room Generation Example: Basically just a randomly generated hallway right now\n')

d = DungeonManager()
gen_params = GenerationProfile(*(np.random.uniform(-1, 1) for x in range(4)))
d.activate(gen_params)

runner = ExampleRunner()
runner.set_room(d.dungeon.rooms[0])
runner.start()
