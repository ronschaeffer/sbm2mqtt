#!/bin/bash

service dbus start
bluetoothd &

./sbm2mqtt.py
