import matplotlib.pyplot as plt
import numpy as np
import math

def calculate_xp_worth(x):
    if x >= 100:
        return 100*x
    return (x/100)*(100*x) + ((100-x)/100) * (10+math.ceil(0.5*x*x + pow(2, math.exp((x-100)/x))))

res = [calculate_xp_worth(x) for x in np.arange(500)]

plt.plot(np.arange(500), res)
print([res[x] for x in range(1,100, 10)])
plt.show()
