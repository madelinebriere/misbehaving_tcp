#!/usr/bin/python

import matplotlib; matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

dupACKs = np.load("npy/dup.npy")
splitACKs = np.load("npy/split.npy")
normalACKs = np.load("npy/normal.npy")
opACKs = np.load("npy/op.npy")
normalACKs_fix = np.load("npy/normal_fix.npy")
opACKs_fix = np.load("npy/op_fix.npy") 

plt.figure(1)
plt.title("Duplicate ACKs")
plt.scatter(dupACKs[0][:-5], dupACKs[1][:-5], 
		label="Duplicate ACKs", color='purple', 
		marker="+")
plt.scatter(normalACKs[0][:-5], normalACKs[1][:-5], 
		label="Normal", color='green', 
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/dup.png")

plt.figure(2)
plt.title("Split ACKs")
plt.scatter(splitACKs[0][:-5], splitACKs[1][:-5],
 		label="Split ACKs", color='magenta',
		marker="+")
plt.scatter(normalACKs[0][:-5], normalACKs[1][:-5], 
		label="Normal", color='green',
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/split.png")

plt.figure(3)
plt.title("Optimistic ACKs")
plt.scatter(opACKs[0][:-5], opACKs[1][:-5],
		 label="Optimistic ACKs", color='blue',
		 marker="+")
plt.scatter(normalACKs[0][:-5], normalACKs[1][:-5], 
		label="Normal", color='green', 
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/op.png")


plt.figure(4)
plt.title("Optimistic ACKs (Fixed)")
plt.scatter(opACKs_fix[0][:-5], opACKs_fix[1][:-5],
		 label="Optimistic ACKs", color='blue',
		 marker="+")
plt.scatter(normalACKs_fix[0][:-5], normalACKs_fix[1][:-5], 
		label="Normal", color='green', 
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/op_fix.png")