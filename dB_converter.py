##Simple script for converting dBm to voltage and vice-versa

import numpy as np

dBm = 17 #power in dBm

P = 1E-3*10**(dBm/10)
V = np.sqrt(P*50) #[V] corresponding voltage for a 50 Ohm system

print(str(dBm)+' dBm = '+str(V)+' V')

V = 2.25
P = V**2/50

dBm = 10*np.log10(P/1e-3)
print(str(V)+' V = '+str(dBm)+' dBm')
#dB = 10*np.log10(P1/P2)