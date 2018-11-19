#!/usr/bin/python

import argparse
import time
import os
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import OVSController

parser = argparse.ArgumentParser(description="Run script")

# What type of script to run. Four options:
# 1. Normal TCP operation
# 2. DupACKing attack from recevier
# 3. OptACKing attack from receiver
# 4. SplitACKing attack from receiver
parser.add_argument("--attack", 
	type=str, 
	choices = ["normal",
    "split",
    "dup",
    "op"],
	default = "normal")

args = parser.parse_args()

# Generate simple topology per Experiment 1.
class NodeGenerator(Topo):
  "Connect two hosts."

  def build(self):
    switch = self.addSwitch('s0')
    server = self.addHost('server', ip='10.0.0.1')
    client = self.addHost('client', ip='10.0.0.2')
    # TODO: Mess with:
    # - RTT
    # - BW
    # - Queue size
    self.addLink(server, switch, bw=200, delay="40ms",
    	loss = 0, max_queue_size = 256)
    self.addLink(client, switch, bw=200, delay="40ms",
    	loss = 0, max_queue_size = 256)
    return


def launchNet():
  topo = NodeGenerator()
  # TODO: Why this controller?
  net = Mininet(topo=topo, 
  	host=CPULimitedHost, 
  	link=TCLink,
  	controller=OVSController)

  print "Starting network"
  net.start()

  print "Retrieving nodes"
  client = net.get('client')
  server = net.get('server')

  # TODO: Determine if this line is necessary
  client.cmd("iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP")

  # Launch webserver to generate traffic
  server.popen("python webserver.py", shell=True)
  #client.popen("python %s %s %s" % (args.script, '10.0.0.1', 8888), shell=True).wait()
  client.popen("python transmit/transmit.py %s %s %d" % (args.attack, '10.0.0.1', 8888), shell=True).wait()

  # Kill webserver
  server.popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait() 
  net.stop()

if __name__ == '__main__':
  launchNet()