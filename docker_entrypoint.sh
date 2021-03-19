#!/bin/bash

service dbus start
bluetoothd &

while true ; do
	./sbm2mqtt.py
	sleep $REPORTING_INTERVAL || break
done
