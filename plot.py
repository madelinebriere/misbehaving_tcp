#!/usr/bin/python

import matplotlib; 
import matplotlib.pyplot as plt
import numpy as np

i=0

# TODO: Make these plots prettier.
for control in ['cubic', 'reno']:

	normal = np.load("normal." + control + ".npy")

	dupACKs = np.load("dup." + control + ".npy")
	plt.figure(i)
	plt.title("DupACKs (%s)" % cong_control)
	plt.scatter(*zip(dup), label="DupACKs")
	plt.scatter(*zip(normal), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Seq Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("dup.%s.png" % (control))

	split = np.load("split." + control + ".npy")
	i=i+1
	plt.figure(i)
	plt.title("SplitACKs (%s)" % control)
	plt.scatter(*zip(split), label="SplitACKs")
	plt.scatter(*zip(normal), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Sequence Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("split.%s.png" % (control))

	op = np.load("op." + control + ".npy")
	i=i+1
	plt.figure(i)
	plt.title("OpACKs (%s)" % cong_control)
	plt.scatter(*zip(op), label="OpACKs")
	plt.scatter(*zip(normal), label="Normal")
	plt.xlabel("Time (s)")
	plt.ylabel("Sequence Number")
	plt.legend(loc="lower right")
	plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	plt.savefig("op.%s.png" % (control))
