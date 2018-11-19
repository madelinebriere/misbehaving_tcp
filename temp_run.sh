mn -c
yes '' | rm output/*.png
yes '' | rm npy/*.npy

sudo python topo_temp.py --attack="normal"
sudo python topo_temp.py --attack="split"
sudo python topo_temp.py --attack="dup"
sudo python topo_temp.py --attack="opt"

python plot.py
