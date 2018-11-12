#!/bin/sh
# Clean up workspace.
sudo mn -c # Clear environment
rm -f *.png
rm -f *.npy

# Run scripts.
sudo python mininetTopo.py --client="normal.py" --control="cubic"
sudo python mininetTopo.py --client="split.py" --control="cubic"
sudo python mininetTopo.py --client="dup.py" --control="cubic"
sudo python mininetTopo.py --client="op.py" --control="cubic"

sudo python mininetTopo.py --client="normal.py" --control="reno"
sudo python mininetTopo.py --client="split.py" --control="reno"
sudo python mininetTopo.py --client="dup.py" --control="reno"
sudo python mininetTopo.py --client="op.py" --control="reno"

# Plot results.
python plot.py
