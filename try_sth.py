import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from scipy import constants
from sympy import *




A, B, C, r = symbols('A,B,C,r')
a = solve(-A/r**2 -B/r**3 - C , r)

print(a, type(a))