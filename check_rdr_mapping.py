import erukar
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D      

e = erukar.engine.factories.DungeonGeneratorRedux()
r = e.generate()

fig = plt.figure()
ax = fig.add_subplot(111)

for start in e.connections:
    for dest in e.connections[start]:
        x = [start[0], dest[0]]
        y = [start[1], dest[1]]

        line = Line2D(x, y)
        ax.add_line(line)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
plt.show()
