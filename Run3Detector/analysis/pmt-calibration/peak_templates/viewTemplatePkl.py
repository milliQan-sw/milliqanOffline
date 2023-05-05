import pickle
import matplotlib.pyplot as plt

# Load in pickled file
dataFile = pickle.load(open('template_peak_70_75_0p2GHz.pkl', 'rb'), encoding='latin1')
print(dataFile) # The data seems to be a list of numbers

fig, ax = plt.subplots()
ax.plot(dataFile)
plt.show()
