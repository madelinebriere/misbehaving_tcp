#! /usr/bin/env python
from scapy.all import *
import random
import sys
import numpy as np
import subprocess as sp

# Information for server (destination).
DST_IP = sys.argv[1]
DST_PORT =  int(sys.argv[2])
control = sys.argv[3]

# Information for client (source), sending ACKs.
SRC_PORT = random.randint(1024,65535)
socket = conf.L2socket(iface="client-eth0")
