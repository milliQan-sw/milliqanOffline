import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

input_template = pickle.load(open("template_peak_70_75_2GHz.pkl", 'rb'))
# input_template = pickle.load(open("template_peak_r7725_400_550_1GHz.pkl", 'rb'))

input_freq = 2.0
output_freq = 1.0
outname = "template_peak_r7725_400_550_0p7GHz.pkl"

orig_times = np.arange(input_template.size)
tmax = orig_times[np.argmax(input_template)]
new_dt = 1.0*(orig_times[-1] - orig_times[0])/(orig_times.size-1) * input_freq / output_freq
print new_dt
new_times = np.append(np.arange(tmax,-new_dt/2,-new_dt)[::-1], np.arange(tmax, orig_times[-1]+new_dt/2, new_dt)[1:])

new_template = []
for i in range(new_times.size):
    t = new_times[i]
    idx = np.argmax(orig_times >= t)
    if idx==0:
        new_template.append(input_template[0])
    else:
        x = input_template[idx-1] + (input_template[idx]-input_template[idx-1])/(orig_times[idx]-orig_times[idx-1]) * (t-orig_times[idx-1])
        new_template.append(x)

# new_template = np.array(new_template) / np.sum(new_template)

print orig_times.size
print new_times.size

# pickle.dump(new_template, open(outname, 'wb'))

plt.plot(orig_times, input_template, 'b-')
plt.plot(new_times, new_template, 'r-')
plt.show()



