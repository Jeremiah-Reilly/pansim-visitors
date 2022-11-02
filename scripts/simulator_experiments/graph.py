import numpy as np
import matplotlib.pyplot as plt

path = 'docs\output\pop_data.npy'
if __name__ == '__main__':
    with open(path):
        x = []
        for _ in range(120):
            y = np.load(file=path)
            value = y[0]
            x.append(value)
    
plt.plot(x)
plt.xlabel("day")
plt.ylabel("population")
plt.show()