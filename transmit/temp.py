#! /usr/bin/env python
from scapy.all import *
import random
import sys
import numpy as np
import subprocess as sp

IP_DST = sys.argv[2]
DST_PORT =  int(sys.argv[3])

IP_SRC = None
SRC_PORT = random.randint(1024,65535)
data = list()
FileName = "npy/normal.npy"

FIN = 0x01

socket = conf.L2socket(iface="client-eth0")

syn = IP(dst=IP_DST) / TCP(window=65535, sport=SRC_PORT, dport=DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport

print "sending SYN....."
syn_ack = sr1(syn)
initialTs = syn_ack.time
initialSeq = syn_ack[TCP].seq
print "Received SYN_ACK!"
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(syn_ack[TCP].ack), ack=(syn_ack[TCP].seq + 1), flags='FA') / getStr

print "Sending Request..."
socket.send(Ether() / request)

def addACKs(pkt):
  global DST_PORT, IP_DST, data, socket
  if IP not in pkt:
    return
  if TCP not in pkt:
    return
  if pkt[IP].src != IP_DST:
    return
  if pkt[TCP].sport != DST_PORT:
    return

  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  
  ip_total_len = pkt.getlayer(IP).len
  ip_header_len = pkt.getlayer(IP).ihl * 32 / 8
  tcp_header_len = pkt.getlayer(TCP).dataofs * 32 / 8
  tcp_seg_len = ip_total_len - ip_header_len - tcp_header_len
  
  add = 0
  if pkt.flags & FIN:
    add = 1

  ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(pkt[TCP].ack), ack=(pkt[TCP].seq + tcp_seg_len), flags='A')
  socket.send(Ether() / ack_pkt)

print("Sniffing......")
sniff(iface="client-eth0", prn=addACKs, filter="tcp and ip", timeout=4)
numbas = np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName, numbas)
