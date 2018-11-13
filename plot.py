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
plt.scatter(*zip(dupACKs), label="Duplicate ACKs", color='purple',
		marker="1")
plt.scatter(*zip(normalACKs), label="Normal", color='green', 
		marker="1")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/dup.png")

plt.figure(2)
plt.title("Split ACKs")
plt.scatter(*zip(splitACKs), label="Split ACKs", color='magenta',
		marker="1")
plt.scatter(*zip(normalACKs), label="Normal", color='green',
		marker="1")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/split.png")

plt.figure(3)
plt.title("Optimistic ACKs")
plt.scatter(*zip(opACKs), label="Optimistic ACKs", color='blue',
		marker="1")
plt.scatter(*zip(normalACKs), label="Normal", color='green', 
		marker="1")
plt.xlabel("Time (s)")
plt.ylabel("Sequence Number")
plt.legend(loc="lower right")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig("output/op.png")
