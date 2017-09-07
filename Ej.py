import numpy as np

h = 6.6e-34
e = 1.6e-19
Phi_0 = h/(2*e)

Ej = 5e-6*1.6e-19

I = Ej*6.28/(Phi_0)


print(repr(I))