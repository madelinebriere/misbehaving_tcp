#!/bin/bash

sudo apt-get update
sudo apt-get -y install python-pip
python -m pip install --upgrade pip
pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
sudo pip install scapy
sudo apt-get -y install mininet
sudo apt-get -y install openvswitch-testcontroller
sudo cp /usr/bin/ovs-testcontroller /usr/bin/ovs-controller

sudo modprobe tcp_vegas
sudo modprobe tcp_cubic
