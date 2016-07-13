import matplotlib.pyplot as plt
import numpy as np
import math

def calc():
    return 4 + np.floor(np.random.standard_cauchy())

res = [calc() for x in np.arange(100000)]
result = [res.count(n)/100000.0 for n in np.arange(min(res), max(res))]

plt.plot(list(np.arange(min(res), max(res))), result)
plt.xlabel('Damage')
plt.ylabel('Probability')

plt.axis([min(res), max(res), -0.05, max(result)+0.05])
plt.show()
