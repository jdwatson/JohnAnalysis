'''
This script calculates the voltage reflection coefficient Gamma
'''

import numpy as np
from matplotlib import pyplot as plt
import qcodes as qc

from scipy import signal as sig
from scipy import interpolate as intpl
import peakutils

from fusion.analysis.SET import staircase as stair

print('hello')


