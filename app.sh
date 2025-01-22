#!/bin/bash

echo "Lista de dispositivos de salida:"
ls /dev/usb/ | grep lp

source foo/bin/activate
python3 main.py 
