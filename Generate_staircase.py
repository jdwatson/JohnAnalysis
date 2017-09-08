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
from fusion.analysis.SET import staircase as stair
from fusion.legacy.spyview_format import SpyViewFormat
spyviewformat = SpyViewFormat()

#*******BEGIN USER INPUT*******
datadir = 'C:/Users/jowat/Desktop/'
datafile = '2017-09-08_001.dat' #2D dataset to import/process
AWG_Vpp = 0.3 #[V] Peak-peak amplitude of AWG signal
waveform_l = 20000 #[samples] length of AWG waveform
down_ramp = 2000 #[samples] length of down sweep
RepRate = 500 #[Hz] AWG repetition rate
#*******END USER INPUT*********


ds1 = qc.load_data(location=datadir+datafile, formatter=spyviewformat)
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




'''
Vg, g_set = stair.loadI(file, 37)

period, mid_pos, xtransfer_fit, g_transfer_fit = stair.transfer(Vg, g_set)

print('Period = '+str(period))
print('mid_pos = '+str(mid_pos))

plt.figure(2)
plt.plot(xtransfer_fit, g_transfer_fit)
plt.xlabel('xtransfer_fit')
plt.ylabel('g_transfer_fit')
plt.title('Transfer function')
'''







plt.show()


