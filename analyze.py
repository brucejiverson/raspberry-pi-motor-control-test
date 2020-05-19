import pickle as pkl
import matplotlib.pyplot as plt


with open('sensor_vals.pkl', 'rb') as f:
    p = pkl.load(f)

plt.plot(p.keys, p.values)
