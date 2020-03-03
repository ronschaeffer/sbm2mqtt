# sqm2mqtt

Grab SwitchBot Meter data over BLE and publish to MQTT topic

Based in part on [OpenWonderLabs/python-host](https://github.com/OpenWonderLabs/python-host) and [Switchbot_Py_Meter](https://github.com/bbostock/Switchbot_Py_Meter)

Intended for use with [Home Assistant](https://github.com/home-assistant/home-assistant.io) but applicable to any system which can use MQTT. Applies to SwitchBot Meter devices with the BLE UUID [https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API](https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API). I don't know if all SwitchBot Meter hardware and firmware versions share the same UUID.

Tested with:

- Pi Zero W running Raspian Buster Lite
- SwitchBot Meters with firmware 2.5

Dependencies:
TBA
