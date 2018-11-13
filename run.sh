mn -c
yes '' | rm output/*.png
yes '' | rm npy/*.npy

sudo python topo.py --script="transmit/normal.py"
sudo python topo.py --script="transmit/split.py"
sudo python topo.py --script="transmit/dup.py"
sudo python topo.py --script="transmit/op.py"

python plot.py
