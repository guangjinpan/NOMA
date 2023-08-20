# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:11:15 2018

@author: lsalaun

© 2016 - 2020 Nokia
Licensed under Creative Commons Attribution Non Commercial 4.0 International
SPDX-License-Identifier: CC-BY-NC-4.0

"""

import numpy as np
import matplotlib.pyplot as plt
import generate_gains
import channel_allocation_JSPA as ca_jspa

K = 5 # Number of users
L = 1 # Number of subcarriers
Multiplex = 3 # Number of users per subcarrier
# Radius of the cell
Radius = 1000
# Min distance between user and BS = 35 m
rmin = 35

#np.random.seed(1)
G = generate_gains.generateGains(K,L,Radius,rmin)

# B : total bandwidth = 5 MHz
B = 5*10**5
W = np.ones(L)*B/L



Pmax = 1.0/L

# Noise value per Hertz = -174 dBm/Hz
Noise_Hz = 10**((-174-30)/10)
N = np.ones(K*L)*Noise_Hz*B/L
N_G = ca_jspa.computeN_G(G,N)

# Decoding order
pi,pi_inv = ca_jspa.computePi(G,N)

print(G,N)
print(N_G)
print(pi,pi_inv,pi.shape)
print(G[pi[0,-1],0],G[pi[0,0],0])

# maxrate=0
# kk=100
# for i in range(0,kk+1):
#     for j in range(0,kk-i+1):
#     # j=kk-i
#         rate1=B/L*np.log2(1+Pmax*i/kk*G[pi[0,-1],0]/N[0])
#         rate2=B/L*np.log2(1+Pmax*j/kk*G[pi[0,0],0]/(Pmax*i/kk*G[pi[0,0],0]+N[0]))
#         rate=rate1+rate2
#         if maxrate<rate:
#             print(rate,rate1,rate2,i,j,G[pi[0,0],0]/N[0],maxrate)
#             maxrate=rate
# rate=B/L*np.log2(1+Pmax*G/N[0])
# print(rate)
# print(Pmax*G/N[0])

G1=G[pi[0,-1],0]
G2=G[pi[0,0],0]

P1=0.2*Pmax
P2=Pmax-P1
rate1=B/L*np.log2(1+P1*G1/(Noise_Hz*B/L))
rate2=B/L*np.log2(1+P2*G2/(P1*G2+Noise_Hz*B/L))
print(rate1,rate2)
rate=rate1+rate2
for i in range(10):
    a1=i*1.0/10
    a2=1-a1
    rate1=a1*B/L*np.log2(1+P1*G1/(Noise_Hz*B/L*a1))
    rate2=a2*B/L*np.log2(1+P2*G2/(Noise_Hz*B/L*a2))
    
    print(rate1,rate2,rate-rate1-rate2)
    rate=rate1+rate2