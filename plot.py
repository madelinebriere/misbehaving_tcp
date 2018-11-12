#!/usr/bin/python

import matplotlib; matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

i=0

for cong_control in ['cubic', 'reno']:

	dupACKs = np.load("npy/dup." + cong_control + ".npy")
	splitACKs = np.load("npy/split." + cong_control + ".npy")
	normalACKs = np.load("npy/normal." + cong_control + ".npy")
	opACKs = np.load("npy/op." + cong_control + ".npy")

	plt.figure(i)
	plt.title("Duplicate ACKs (%s)" % cong_control)
	plt.scatter(*zip(dupACKs), label="Duplicate ACKs")
	plt.scatter(*zip(normalACKs), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Sequence Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("output/dup.%s.png" % cong_control)
	i=i+1

	plt.figure(i)
	plt.title("Split ACKs (%s)" % cong_control)
	plt.scatter(*zip(splitACKs), label="Split ACKs")
	plt.scatter(*zip(normalACKs), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Sequence Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("output/split.%s.png" % cong_control)
	i=i+1

	plt.figure(i)
	plt.title("Optimistic ACKs (%s)" % cong_control)
	plt.scatter(*zip(opACKs), label="Optimistic ACKs")
	plt.scatter(*zip(normalACKs), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Sequence Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("output/op.%s.png" % cong_control)
