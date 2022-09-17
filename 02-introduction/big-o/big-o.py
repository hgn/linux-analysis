#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Big-O   	Name
# 1   		Constant
# log(n)  	Logarithmic
# n   		Linear
# nlog(n) 	Log Linear
# n^2 		Quadratic
# n^3 		Cubic
# 2^n 		Exponential


import numpy as np
import matplotlib
import matplotlib.pyplot as plt

font = {
        'weight' : 'normal',
        'size'   : 17}

matplotlib.rc('font', **font)


# Stylesheets defined in Matplotlib
##plt.style.use('bmh')

# Set up runtime comparisons
n = np.linspace(1, 100, 1000)
labels = ['Constant - O(1)', 'Logarithmic - O(log n)', 'Linear O(n)', 'Log Linear O(n * log n)', 'Quadratic O(n^2)', 'Exponential O(2^n)']
big_o = [np.ones(n.shape), np.log(n), n, n * np.log(n), n**2, 2**n]

# Plot setup
plt.figure(figsize=(18, 10))
plt.ylim(0, 100)

for i in range(len(big_o)):
    plt.plot(n, big_o[i], label=labels[i], linewidth=4.0)

plt.legend(loc=0)
plt.ylabel('Relative Runtime')
plt.xlabel('Input Size')
plt.savefig('big-o-notation.png', bbox_inches='tight', dpi=300, transparent=True)
