from erukar import Lifeform
from erukar.engine.managers.TurnManager import TurnManager

t = TurnManager()

s = Lifeform()
s.name = "Slow Guy"
t.subscribe(s)

f = Lifeform()
f.dexterity = 8
f.name = "Fast Guy"
t.subscribe(f)

turn_order = t.turn_order()

for i in range(99):
    guy, count = next(turn_order)
    print('{0}:\t{1} ({2})'.format(count,guy.name, guy.turn_modifier()))
