sudo mn -c
yes '' | rm output/*.png
yes '' | rm npy/*.npy

sudo python topo.py --attack="normal"
sudo python topo.py --attack="split"
sudo python topo.py --attack="dup"
sudo python topo.py --attack="op"

python plot.py
