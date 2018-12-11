sudo mn -c
yes '' | rm output/*.png
yes '' | rm npy/*.npy

sudo python topo.py --attack="normal" --fix=0
sudo python topo.py --attack="normal" --fix=1
sudo python topo.py --attack="split" --fix=0
sudo python topo.py --attack="dup" --fix=0
sudo python topo.py --attack="op" --fix=0
sudo python topo.py --attack="op" --fix=1

python plot.py
