##Simple script for converting dBm to voltage and vice-versa

import numpy as np

dBm = 17 #power in dBm

P = 1E-3*10**(dBm/10)
V = np.sqrt(P*50) #[V] corresponding voltage for a 50 Ohm system

print(str(dBm)+' dBm = '+str(V)+' V')

#dB = 10*np.log10(P1/P2)