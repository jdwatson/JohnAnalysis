'''
This script converts a 2D dataset of SET response vs SET gate and box gate into a Coulomb staircase dataset.
It assumes the SET gate was swept slowly (e.g. with a DAC) while the box gate was ramped with an AWG along the x axis
'''

import numpy as np
from matplotlib import pyplot as plt
import qcodes as qc
from scipy import signal as sig
from scipy import interpolate as intpl
import peakutils
from fusion.analysis.SET import gen_transfer as gen_trans
from fusion.analysis.SET import staircase as stair
from fusion.legacy.spyview_format import SpyViewFormat
spyviewformat = SpyViewFormat()

#*******BEGIN USER INPUT*******

datadir = 'C:/Users/jowat/Desktop/'
datafile = '2017-09-09_008.dat' #2D dataset to import/process
AWG_Vpp = 0.3 #[V] Peak-peak amplitude of AWG signal
waveform_l = 20000 #[samples] length of AWG waveform
down_ramp = 2000 #[samples] length of down sweep
RepRate = 500 #[Hz] AWG repetition rate
transfer_start = 1.916 #[V] Value in SET gate at which to start transfer function
transfer_end = 1.919 #[V] Value in SET gate at which to end transfer function
transfer_cut = 0.15 #[V] Value in AWG voltage at which to make a line cut for the transfer function
SET_period = 0.0158 #SET blockade periodicity in same units as data (e.g. Volts)
kappa = 0.033 #0.02 #Ratio of box-SET coupling capacitance to box total capacitance
box_period = 0.027 #1e in units of AWG voltage
SET_gate_cut = 1.91767 #[V] position in SET gate at which to make a staircase linecut

#*******END USER INPUT*********




'''
Algorithm: 
1) Import the raw data to and plot as a sanity check that you imported the right dataset
2) Use the y-sweep data (e.g. SET gate) to generate the transfer curve over the user-defined range
3) Use this transfer curve to convert RF amplitude vs box gate voltage to SET charge vs box gate charge
4) Using the user-defined coupling constant kappa, convert SET charge vs box gate charge to average box charge vs box gate charge
'''

ds1 = qc.load_data(location=datadir+datafile, formatter=spyviewformat)

#Convert time axis to AWG voltage
period = 1/RepRate
up_time = period*(waveform_l - down_ramp)/waveform_l
V_conversion = AWG_Vpp/up_time #[V/s]


#Plot the full 2D dataset as a sanity check
X = V_conversion*ds1.DataArray0[0, 0, :]
Y = ds1.DataArray1[0, :]
Z = ds1.DataArray3[0, :, :] #Not sure what first index is.  Second index corresponds to a particular y value, third index corresponds to a particular x value
plt.figure(1)
plt.pcolormesh(X,Y,Z)
plt.xlabel('AWG V (V)')
plt.ylabel('SET Gate (V)')
plt.title(datafile)
plt.colorbar()


#Find the index positions of the start and end of the transfer function
eps1 = 1e-3
for i in range(len(Y)):
    if (np.abs(Y[i] - transfer_start) < eps1):
        transfer_start_ind = i
    if (np.abs(Y[i] - transfer_end) < eps1):
        transfer_end_ind = i

if transfer_start_ind > transfer_end_ind:
    temp = transfer_end_ind
    transfer_end_ind = transfer_start_ind
    transfer_start_ind = temp

#Find the AWG voltage index position corresponding to the desired line cut for the transfer function
eps2 = 1e-3
for i in range(len(X)):
    if (np.abs(X[i] - transfer_cut) < eps2):
        transfer_cut_ind = i


x_trans, y_trans, degen_ind = gen_trans.AWG_Transfer(Y, Z[:,transfer_cut_ind], transfer_start_ind, transfer_end_ind, SET_period, 8)
ng_SET = Y/SET_period + (0.5 - Y[degen_ind]/SET_period)

plt.figure(2)
plt.plot(ng_SET, Z[:,transfer_cut_ind], label='Raw data')
plt.plot(x_trans, y_trans, 'o', label='Transfer function')
plt.xlabel('SET Gate (e)')
plt.ylabel('SET response')
plt.title('Transfer function check')
plt.legend(loc='lower left')


def use_transfer(SET_response, x_transfer, y_transfer):
    q_set = np.empty(len(SET_response))
    for i in range(len(SET_response)):
        idx = np.argmin(np.abs(y_transfer- SET_response[i]))
        q_set[i] = x_transfer[idx]

    return q_set

Q_SET = np.empty(Z.shape)
for i in range(len(Y)):
    Q_SET[i, :] = use_transfer(Z[i,:], x_trans, y_trans)


plt.figure(3)
plt.pcolormesh(X,ng_SET,Q_SET)
plt.xlabel('AWG V (V)')
plt.ylabel('ng_SET (e)')
plt.title('Q_SET (e)')
plt.colorbar()

'''
hor_linecut_val = 0.433 #[e]
for i in range(len(ng_SET)):
    hor_linecut_ind = np.argmin(np.abs(ng_SET - hor_linecut_val))
'''

for i in range(len(Y)):
    hor_linecut_ind = np.argmin(np.abs(Y - SET_gate_cut))
ng_Box = X/box_period

plt.figure(4)
plt.plot(ng_Box, Q_SET[hor_linecut_ind, :])
plt.xlabel('ng_Box (e)')
plt.ylabel('Q_SET (e)')
plt.title('Line cut after using transfer function. SET gate = '+str(Y[hor_linecut_ind])+'V')

plt.figure(5)
plt.plot(ng_Box, Z[hor_linecut_ind, :])
plt.xlabel('ng_Box (e)')
plt.ylabel('RF Amplitude (V)')
plt.title('Line cut before using transfer function')

def Q_SET_to_Q_Box(ng_box, q_set, coupling_constant):
    Q_Box = np.empty(len(ng_box))
    for i in range(len(ng_box)):
        Q_Box[i] = ng_box[i] - q_set[i]/coupling_constant
    return Q_Box


ng_Box = X/box_period
Q_BOX = np.empty(Q_SET.shape)
for i in range(len(Q_SET)):
    Q_BOX[i, :] = Q_SET_to_Q_Box(ng_Box, Q_SET[i, :], kappa)


plt.figure(6)
plt.plot(ng_Box, Q_BOX[hor_linecut_ind, :])
plt.xlabel('ng_Box')
plt.ylabel('Q_BOX (e)')
plt.title('Line cut of box charge. Kappa = '+str(kappa))
plt.xticks(np.arange(min(ng_Box), max(ng_Box)+1, 1.0))
plt.yticks(np.arange(int(min(Q_BOX[hor_linecut_ind,:])), int(max(Q_BOX[hor_linecut_ind,:])+1), 1.0))
plt.grid(color='k', linestyle='--', linewidth=0.75)

plt.figure(7)
plt.pcolormesh(ng_Box, ng_SET, Q_BOX)
plt.xlabel('n_g_Box (e)')
plt.ylabel('ng_SET (e)')
plt.title('Q_BOX (e)')
plt.colorbar()





#
# Q_SET = np.empty((len(X),len(Y)))
# Q_BOX = np.empty((len(X),len(Y)))
# for i in range(len(Y)):
#     Q_SET[:, i], Q_BOX[:, i] = stair.staircase(X / SET_period, Z[i, :], k_coupling, x_trans, y_trans)
# '''
# Q_SET, Q_BOX = stair.staircase(X / SET_period, Z[0, :], k_coupling, x_trans, y_trans)
#
# plt.figure(3)
# plt.plot(X,Q_SET)
# plt.title('Q_SET')
#
# plt.figure(4)
# plt.plot(X, Q_BOX)
# plt.title('Q_BOX')
#
# '''
# plt.figure(3)
# plt.pcolormesh(X,Y,np.transpose(Q_SET))
# plt.xlabel('AWG V (V)')
# plt.title('Q_SET')
# plt.colorbar()
#
# plt.figure(4)
# plt.pcolormesh(X,Y,np.transpose(Q_BOX))
# plt.ylabel('SET Gate (V)')
# plt.xlabel('AWG V (V)')
# plt.ylabel('SET Gate (V)')
# plt.title('Q_BOX')
# plt.colorbar()


plt.show()


