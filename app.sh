#!/bin/bash

echo "Lista de dispositivos de salida:"
ls /dev/usb/ | grep lp

source foo/bin/activate
export FLASK_DEBUG=1
export FLASK_APP=main
flask run --host=0.0.0.0
