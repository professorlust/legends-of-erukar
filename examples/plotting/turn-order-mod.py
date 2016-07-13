import matplotlib.pyplot as plt
import math

def tom(d):
    return 10+40* (1 - 1 / (1 + math.exp( (10-d) / 5 ) ) )

result = [tom(d) for d in range(-2,21)]
plt.plot(list(range(-2,21)), result)
plt.xlabel('Dexterity')
plt.ylabel('Turn Order Modifier')

plt.axis([-2, 20, 10, 50])
plt.show()
