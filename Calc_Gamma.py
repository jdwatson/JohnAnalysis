'''
This script calculates the voltage reflection coefficient Gamma
'''

import numpy as np
from matplotlib import pyplot as plt
import qcodes as qc
from fusion.legacy.spyview_format import SpyViewFormat
spyviewformat = SpyViewFormat()

#**************
#USER INPUT

datafile = 'C:/Users/jowat/Desktop/2017-09-06_033'
horiz_line_val = 431.3E6 #[Hz] horizontal linecut value to plot
gate_blockade = 1.825 #Value of gate for which device is in blockade (e.g. assume fully reflecting)
gate_res = 1.8132
#END USER INPUT
#**************

eps1 = 5E5 #[Hz] Max error in looking for linecut at constant frequency
eps2 = 3E-4 #[V] Max error in looking for lincut at constant voltage

#Load the dataset
ds1 = qc.load_data(location=datafile, formatter=spyviewformat)

#Plot the raw data as a sanity check
X = ds1.DataArray0[0, 0, :]
Y = ds1.DataArray1[0, :]
Z = ds1.DataArray3[0, :, :] #Not sure what first index is.  Second index corresponds to a particular y value, third index corresponds to a particular x value
plt.figure(1)
plt.pcolormesh(X,Y,Z)
plt.xlabel('S1P (V)')
plt.ylabel('Frequency (Hz)')
plt.colorbar()
plt.title('Raw data')

#Plot a horizontal linecut at a particular index

for i in range(len(Y)):
    if (np.abs(Y[i] - horiz_line_val) < eps1):
        horiz_line_ind = i


linecut_label = 'f = '+str(Y[horiz_line_ind]/1e6)+' MHz'
plt.figure(2)
plt.plot(X,Z[horiz_line_ind,:])
plt.xlabel('S1P (V)')
plt.ylabel('CH1 (V)')
plt.title(linecut_label)



V_ref = Z[0,0]

#Convert datset to S11 assuming tank circuit is fully reflecting far from resonance (e.g. first data point)
S11 = np.empty([len(X),len(Y)], dtype=float)
for i in range(len(X)):
    for j in range(len(Y)):
        S11[i,j] = 20*np.log10(Z[i,j]/V_ref)

plt.figure(3)
plt.pcolormesh(X,Y,S11)
plt.xlabel('S1P (V)')
plt.ylabel('Frequency (Hz)')
plt.title('S11 (dB)')
plt.colorbar()

plt.figure(4)
plt.plot(X,S11[horiz_line_ind,:])
plt.xlabel('S1P (V)')
plt.ylabel('S11 (dB)')
plt.title(linecut_label)


for i in range(len(X)):
    if (np.abs(X[i] - gate_blockade) < eps2):
        gate_blockade_ind = i
    if (np.abs(X[i] - gate_res) < eps2):
        gate_res_ind = i

blockade_label = 'Blockade, Gate = '+str(X[gate_blockade_ind])
res_label = 'Resonance, Gate = '+str(X[gate_res_ind])
plt.figure(5)
plt.plot(Y, S11[:, gate_blockade_ind], label = blockade_label )
plt.plot(Y, S11[:, gate_res_ind], label = res_label)
plt.xlabel('Frequency (Hz)')
plt.ylabel('S11 (dB)')
plt.title('Voltage linecuts')
plt.legend(loc = 'lower left')

#Now calculate change in S11 between blockade and resonance
Delta_S11 = np.empty([len(X),len(Y)], dtype=float)
for i in range(len(X)):
    for j in range(len(Y)):
        Delta_S11[i,j] = S11[i, j] - S11[i, gate_blockade_ind]

plt.figure(6)
plt.pcolormesh(X, Y, Delta_S11)
plt.xlabel('S1P (V)')
plt.ylabel('Frequency (Hz)')
plt.title('Delta S11 (dB)')
plt.colorbar()

#Last, convert this difference in S11 to Gamma
Gamma = np.empty([len(X),len(Y)], dtype=float)
for i in range(len(X)):
    for j in range(len(Y)):
        Gamma[i,j] = 10**Delta_S11[i, j]


plt.figure(7)
plt.pcolormesh(X, Y, Gamma)
plt.xlabel('S1P (V)')
plt.ylabel('Frequency (Hz)')
plt.title('|Gamma|^2')
plt.colorbar()

plt.figure(8)
plt.plot(X,Gamma[horiz_line_ind,:])
plt.xlabel('S1P (V)')
plt.ylabel('|Gamma|^2')
plt.title(linecut_label)


plt.figure(9)
plt.plot(Y, Gamma[:, gate_res_ind], label = res_label)
plt.xlabel('Frequency (Hz)')
plt.ylabel('|Gamma|^2 (dB)')
plt.title('Gamma linecuts')
plt.legend(loc = 'lower left')


plt.show()
