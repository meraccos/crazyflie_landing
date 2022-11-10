#!/bin/bash

apt-get update && apt-get upgrade
apt-get install sudo git vim python python3 python3-pip

sudo apt install libxcb-xinerama0
pip3 install --upgrade pip

sudo apt-get update -y
sudo apt-get install -y udev

sudo groupadd plugdev
sudo usermod -a -G plugdev $USER

cat <<EOF | sudo tee /etc/udev/rules.d/99-bitcraze.rules > /dev/null
# Crazyradio (normal operation)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"
# Bootloader
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", GROUP="plugdev"
# Crazyflie (over USB)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"
EOF

pip3 install cfclient