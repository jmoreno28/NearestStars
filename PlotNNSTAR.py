import numpy as np
import math as math
import cmath as cmath
import psutil as psutil
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from matplotlib import gridspec as gridspec
import argparse as argparse
import operator as operator
import warnings as warnings
import copy as copy
import time as time
import pdb
import os as os
import random

import kali.k2
import kali.s82
import kali.carma
import kali.util.mcmcviz as mcmcviz
from kali.util.mpl_settings import set_plot_params


def doubleMADsfromMedian(y,thresh=3.):
    # warning: this function does not check for NAs
    # nor does it address issues when 
    # more than 50% of your data have identical values
    m = np.median(y)
    abs_dev = np.abs(y - m)
    left_mad = np.median(abs_dev[y <= m])
    right_mad = np.median(abs_dev[y >= m])
    y_mad = left_mad * np.ones(len(y))
    y_mad[y > m] = right_mad
    modified_z_score = 0.6745 * abs_dev / y_mad
    modified_z_score[y == m] = 0
    return np.where(modified_z_score < thresh)[0]
    




#---------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('-id', '--id', type = str, default = '220173631', help = r'EPIC ID')
parser.add_argument('-starid', '--starid', type = str, default = '220172755', help = r'EPIC ID')
parser.set_defaults(viewer = True)
args = parser.parse_args()

id = args.id
star_id = args.starid



k2lc = kali.k2.k2LC(name = id, band = 'Kep', processing = 'k2sff', campaign = 'c08')
k2lcStar = kali.k2.k2LC(name = star_id, band = 'Kep', processing = 'k2sff', campaign = 'c08')
w = np.where(k2lc.mask > 0)[0]
w2 = np.where(k2lcStar.mask > 0)[0]

z = doubleMADsfromMedian(k2lc.y )
z2 = doubleMADsfromMedian(k2lcStar.y )

k2lc.mask = np.zeros(len(k2lc.y))
k2lc.mask[z] = 1
k2lc.cadence = np.arange(0,len(k2lc.y))


k2lcStar.mask = np.zeros(len(k2lcStar.y))
k2lcStar.mask[z2] = 1
k2lcStar.cadence = np.arange(0,len(k2lcStar.y))

import seaborn as sns

sns.palplot(sns.color_palette("GnBu_d"))

f, (ax, ax2) = plt.subplots(1, 2, sharey=False)
ax.fill_between(k2lc.t[z],k2lc.y[z]-k2lc.yerr[z], k2lc.y[z]+k2lc.yerr[z], color='c', alpha=0.2)
ax.scatter(k2lcStar.t[z2],k2lcStar.y[z2],  marker = "+",color =  'm', label=str("K2 Star "+star_id))
ax.scatter(k2lc.t[z],k2lc.y[z],  marker = "+",color =  '#ff7f00', label=str("K2 QSO"+id))
ax.set_xlim(k2lc.t[0], k2lc.t[-1])  
ax.set_ylim(0.6, 1.3)  

Stary = k2lcStar.y/np.median(k2lcStar.y)
ax2.fill_between(k2lcStar.t[z2],(k2lcStar.y[z2]-k2lcStar.yerr[z2])/np.median(k2lcStar.y), (k2lcStar.y[z2]+k2lcStar.yerr[z2])/np.median(k2lcStar.y), color='m', alpha=0.2)
ax2.scatter(k2lcStar.t[z2],Stary[z2],  marker = "+",color =  'm', label=str("K2 Star "+star_id))
ax2.set_xlim(k2lcStar.t[0], k2lcStar.t[-1])  
#ax2.set_ylim(0.6, 1.3)  
ax.legend(loc="upper left", prop={'size':15})
ax2.legend(loc="upper left", prop={'size':15})
ax.set_ylabel('Relative Flux', fontsize = 12)
ax.set_xlabel('time [days]', fontsize = 12)
ax2.set_xlabel('time [days]', fontsize = 12)
f.subplots_adjust(hspace=0.01)
f.tight_layout()
f.savefig(id+'NearestNeighbor.png', dpi=400)
