#!/usr/bin/env bash

# USB 3.1 Only
for port in $(lspci | grep xHCI | cut -d' ' -f1); do
    echo -n "0000:${port}"| sudo tee /sys/bus/pci/drivers/xhci_hcd/unbind;
    sleep 1;
    echo -n "0000:${port}" | sudo tee /sys/bus/pci/drivers/xhci_hcd/bind;
    sleep 1;
done
