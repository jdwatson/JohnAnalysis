import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('C:/Users/jowat/Downloads/OneDrive-2017-06-21/2017-06-21_005.dat',dtype=None,skiprows=28)

conditional_data = np.zeros((401,2))
f_cut = 251227636.18190905
#condition = data == f_cut
j=0
for i in range(len(data[:,0])):
    if data[i,0] == f_cut:
        conditional_data[j,0] = data[i,1]
        conditional_data[j,1] = data[i,4]
        j = j + 1
plt.plot(conditional_data[:,0],conditional_data[:,1])
plt.show()

np.savetxt('D:/jwatson/Downloads/2017-06-02_044_linecut3.txt', conditional_data, delimiter='\t')