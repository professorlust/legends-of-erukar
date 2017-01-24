import os, sys
sys.path.append(os.getcwd())

from erukar import *
import erukar

dungeon = Dungeon()
dungeon.name = "Barlen Town Center"
dungeon.sovereignty = 'Iuria'
dungeon.region = "Town of Barlen"
dungeon.description = "The Barlen Town Center is a hub of activity for marketgoers and craftsmen in the Lesser Iurian Woodlands. The Town Center is home to various guilds -- the Barlen Baker's Guild and a small adventuring guild known as \"Consultants and Dragons\", to name a few.\nBarlen itself is a day's journey from Oridel and a bit longer from the Iurian capital, Luinden."

'''Consultants and Dragons'''
# Guild Hall Antechamber (0, 0)
gh_antechamber = Room(dungeon, (0,0))
gh_antechamber.SelfDescription = 'This is the antechamber to an adventurer\'s guild named "Consultants and Dragons."'

t = Torch()
t.fuel = 100
gh_antechamber.add(t)

dummy_room = Room(dungeon, (1,0), dimensions=(1,1))
gh_antechamber.coestablish_connection(Direction.East, dummy_room, InstanceTransition('Instance transition door', 'TutorialDungeon'))

m = Sword()
erukar.game.modifiers.material.Abyssium().apply_to(m)
erukar.game.modifiers.random.Flaming().apply_to(m)
gh_antechamber.add(m)

# Guild Hall Hallway (0, 1)
gh_hallway = Room(dungeon, (0,1))
gh_hallway.SelfDescription = 'The hallway connects to several rooms.'
gh_antechamber.coestablish_connection(Direction.North, gh_hallway)

# Guild Hall Meeting Room (1,1)
# Guild Hall Stock Room (2, 1)

'''Barlen Way'''
# Outside of Consultants and Dragons (0, -1)
barlen_way = Room(dungeon, (0, -1))
barlen_way.SelfDescription = 'The busy street known as "Barlen Way" extends from the East to the West. To your North you see a three story concrete building with red and black flags hanging from the windows, and to your South you see a sign that reads "The Tipsy Sorcerer."'
barlen_way.coestablish_connection(Direction.North, gh_antechamber, Door())

barlen_way_e = Room(dungeon, (1, -1), dimensions=(3,1))
barlen_way_e.SelfDescription = 'To your north you see a three story concrete building with red and black flags hanging from the windows, and to your South you see a sign that reads "The Tipsy Sorcerer."'
barlen_way.coestablish_connection(Direction.East, barlen_way_e)

barlen_way_ee = Room(dungeon, (4,-2), dimensions=(3,3), shape=erukar.engine.environment.roomshapes.Cross)
barlen_way_ee.SelfDescription = 'Barlen Way intersects with an alley that goes between the northern concrete building and the tavern to the south.'
barlen_way_e.coestablish_connection(Direction.East, barlen_way_ee)

barlen_way_w = Room(dungeon, (-3, -1), dimensions=(3,1))
barlen_way_w.SelfDescription = 'An armored guard stands to the north in this section of the Barlen Way. He nods to you as you glance at him. Behind him to the north you see a three story concrete building with red and black flags hanging from the windows, and to South of the streetyou see a sign that reads "The Tipsy Sorcerer."'
barlen_way.coestablish_connection(Direction.West, barlen_way_w)

barlen_way_ww = Room(dungeon, (-2, -1))
barlen_way_ww.SelfDescription = 'Barlen Way intersects with an alley that goes between the northern concrete building and the tavern to the south.'
#barlen_way_w.coestablish_connection(Direction.West, barlen_way_ww)

cnd_alley_sw = Room(dungeon, (-2, 0))
cnd_alley_sw.SelfDescription = 'alley'
#barlen_way_ww.coestablish_connection(Direction.North, cnd_alley_sw)

'''The Tipsy Sorcerer'''
# Main Area (0, -2)
tipsy_sorcerer = Room(dungeon, (0, -3), dimensions=(2,2))
tipsy_sorcerer.SelfDescription = 'The Tipsy Sorcerer is a tavern for academics and artists. Rows of tables are topped with red cloths embroidered with "TTS" monograms. Some of the tables have candles on top and a few even come with complimentary inkwells. The bar stands at the northern side of the main room.'
tipsy_sorcerer.coestablish_connection(Direction.North, barlen_way, Door())

tipsy_sorcerer_stockroom = Room(dungeon, (2, -3), dimensions=(1,2))
tipsy_sorcerer_stockroom.coestablish_connection(Direction.West, tipsy_sorcerer, Door())
