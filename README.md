# sqm2mqtt
Grab SwitchBot Meter data over BLE and publish to MQTT topic

Based in part on https://github.com/OpenWonderLabs/python-host
Inspired by https://github.com/bbostock/Switchbot_Py_Meter

Intended for use with @homeassistant but applicable to any system which can use MQTT. Applies to SwitchBot Meter devices with the BLE UUID cba20d00-224d-11e6-9fb8-0002a5d5c51b https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API. I don't know if all SwitchBot Meter hardware and firmware versions share the same UUID.

Tested with:
- Pi Zero W running Raspian Buster Lite
- SwitchBot Meters with firmware 2.5

Dependencies:
TBA

