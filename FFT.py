'''
This script does a line-by-line 1D FFT of a 2D dataset.  Initially intended for finding periodicity of Coulomb staircase data
'''

import numpy as np
from matplotlib import pyplot as plt
import qcodes as qc
from fusion.legacy.spyview_format import SpyViewFormat


spyviewformat = SpyViewFormat()
'''
t = np.linspace(0,7,500)
data = np.sin(2*np.pi*(t)) + np.sin(6*np.pi*(t))


plt.figure(1)
plt.plot(t,data)
plt.xlabel('t')
plt.ylabel('data')
plt.show()

transform = np.fft.fft(data)
#freq = np.fft.fftfreq(len(t), t[1]-t[0])
freq = np.linspace(0.0, 1/(2*(t[1]-t[0])), len(t)/2)

plt.figure(2)
plt.plot(freq, np.abs(transform[0:int(len(data)/2)]))
plt.xlabel('Frequency')
plt.ylabel('Transform')
plt.show()
'''


ds1 = qc.load_data(location='C:/Users/jowat/Desktop/2017-09-06_050', formatter=spyviewformat)
plt.figure(1)
plt.plot(ds1.DataArray0[0,0,:], ds1.DataArray3[0,0,:], label = 'First line trace')
plt.plot(ds1.DataArray0[0,0,:], ds1.DataArray3[0,1,:], label = 'Second line trace')
plt.legend(loc='upper right')
plt.xlabel('Time (s)')
plt.ylabel('CH1 Amplitude (V)')
#plt.show()
#ax = plot1d(ds1, [[3]], show=False)

plt.figure(2)
plt.plot(166.7*ds1.DataArray0[0,0,:], ds1.DataArray3[0,0,:], label = 'First line trace')
plt.plot(166.7*ds1.DataArray0[0,0,:], ds1.DataArray3[0,1,:], label = 'Second line trace')
plt.legend(loc='upper right')
plt.xlabel('AWG ramp (V)')
plt.ylabel('CH1 Amplitude (V)')
#plt.show()

V = 166.7*ds1.DataArray0[0, 0, :]
Amp = ds1.DataArray3[0, 0, :]

#V_trans = np.fft.fftfreq(len(V),V[1]-V[0])
V_trans = np.linspace(0.0, 1/(2*(V[1]-V[0])), len(V)/2)
Amp_trans = np.fft.fft(Amp)

plt.figure(3)
plt.plot(V_trans, Amp_trans[0:len(V_trans)], )
plt.xlabel('1/V')
plt.ylabel('FFT')
x1,x2,y1,y2 = plt.axis()
plt.axis((x1, 100, 0, 0.5))
#plt.show()

X = 166.7*ds1.DataArray0[0, 0, :]
Y = ds1.DataArray1[0, :]
Z = ds1.DataArray3[0, :, :] #Not sure what first index is.  Second index corresponds to a particular y value, third index corresponds to a particular x value


plt.figure(4)
plt.pcolormesh(X,Y,Z)
plt.xlabel('AWG V (V)')
plt.ylabel('S1P (V)')
plt.colorbar()
#plt.show()


#X_trans = np.fft.fftfreq(len(X),X[1]-X[0])
X_trans = np.linspace(0.0, 1/(2*(X[1] - X[0])), len(X)/2)
Y_trans = Y
Z_trans = Z

for i in range(len(Y)):
    temp = np.fft.fft(Z[i, :])
    for j in range(len(X)):
        Z_trans[i, j] = temp[j]

plt.figure(5)
plt.pcolormesh(X_trans, Y_trans, Z_trans[:, 0:len(X_trans)], vmin=0, vmax=0.2)
plt.xlim(0,100)
plt.xlabel('Inverse V (1/V)')
plt.ylabel('S1P (V)')
plt.colorbar()
plt.show()


