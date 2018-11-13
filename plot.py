#!/usr/bin/python

import matplotlib; matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

dupACKs = np.load("npy/dup.npy")
splitACKs = np.load("npy/split.npy")
normalACKs = np.load("npy/normal.npy")
opACKs = np.load("npy/op.npy")

plt.figure(1)
plt.title("Duplicate ACKs")
plt.scatter(dupACKs[0][:-3], dupACKs[1][:-3], 
		label="Duplicate ACKs", color='purple', 
		marker="+")
plt.scatter(normalACKs[0][:-3], normalACKs[1][:-3], 
		label="Normal", color='green', 
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/dup.png")

plt.figure(2)
plt.title("Split ACKs")
plt.scatter(splitACKs[0][:-3], splitACKs[1][:-3],
 		label="Split ACKs", color='magenta',
		marker="+")
plt.scatter(normalACKs[0][:-3], normalACKs[1][:-3], 
		label="Normal", color='green',
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/split.png")

plt.figure(3)
plt.title("Optimistic ACKs")
plt.scatter(opACKs[0][:-3], opACKs[1][:-3],
		 label="Optimistic ACKs", color='blue',
		 marker="+")
plt.scatter(normalACKs[0][:-3], normalACKs[1][:-3], 
		label="Normal", color='green', 
		marker="+")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/op.png")
