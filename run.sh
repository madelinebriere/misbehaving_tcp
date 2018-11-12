mn -c
yes '' | rm output/*.png
yes '' | rm npy/*.npy

sudo python topo.py --script="transmit/normal.py" --control="cubic"
sudo python topo.py --script="transmit/split.py" --control="cubic"
sudo python topo.py --script="transmit/dup.py" --control="cubic"
sudo python topo.py --script="transmit/op.py" --control="cubic"

sudo python topo.py --script="transmit/normal.py" --control="reno"
sudo python topo.py --script="transmit/split.py" --control="reno"
sudo python topo.py --script="transmit/dup.py" --control="reno"
sudo python topo.py --script="transmit/op.py" --control="reno"

python plot.py
