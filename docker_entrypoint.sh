#!/bin/bash

service dbus start
bluetoothd &

while true ; do
	./sbm2mqtt.py
	sleep $MQTT_INTERVAL || break
done
