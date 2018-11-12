
sudo python mininetTopo.py --client="normal" --server="linux" --cong-control="cubic"
sudo python mininetTopo.py --client="splitACK" --server="linux" --cong-control="cubic"
sudo python mininetTopo.py --client="dupACK" --server="linux" --cong-control="cubic"
sudo python mininetTopo.py --client="opACK" --server="linux" --cong-control="cubic"

sudo python mininetTopo.py --client="normal" --server="linux" --cong-control="reno"
sudo python mininetTopo.py --client="splitACK" --server="linux" --cong-control="reno"
sudo python mininetTopo.py --client="dupACK" --server="linux" --cong-control="reno"
sudo python mininetTopo.py --client="opACK" --server="linux" --cong-control="reno"

# sudo python mininetTopo.py --client="normal" --server="linux" --cong-control="vegas"
# sudo python mininetTopo.py --client="splitACK" --server="linux" --cong-control="vegas"
# sudo python mininetTopo.py --client="dupACK" --server="linux" --cong-control="vegas"
# sudo python mininetTopo.py --client="opACK" --server="linux" --cong-control="vegas"

python plot.py
sudo python -m SimpleHTTPServer 80
