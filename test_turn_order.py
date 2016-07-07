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

for i in range(99):
    guy = t.next()
    print('{0} ({1})'.format(guy.name, guy.turn_modifier()))
