# sbm2mqtt

Grab SwitchBot Meter data over BLE and publish to MQTT topic for Home Assistant, etc.

- Based in part on [OpenWonderLabs/python-host](https://github.com/OpenWonderLabs/python-host), [Switchbot_Py_Meter](https://github.com/bbostock/Switchbot_Py_Meter) and [switchbot-meter.py](https://qiita.com/warpzone/items/11ec9bef21f5b965bce3).
- Intended for use with [Home Assistant](https://github.com/home-assistant/home-assistant.io) but applicable to any system which can use MQTT.
- Applies to SwitchBot Meter devices with the BLE UUID [cba20d00-224d-11e6-9fb8-0002a5d5c51b](https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API). I don't know if all SwitchBot Meter hardware and firmware versions share the same UUID.

Tested with:

- Pi Zero W & Pi 3B+ running Raspbian Buster Lite 2020-02-13
- SwitchBot Meters with firmware 2.5
- Python 3.7.3
- Local MQTT broker
- Home Assistant 0.106 configured to connect to the local MQTT broker (optional) 

### Background

**TL;DR** Start with a fresh install of Raspbian Buster Lite. Don't install the dependencies recommended by OpenWonderLabs for python-host.

OpenWonderLabs published the open API for SwitchBot Meters in late 2019. [bbostock](https://github.com/bbostock) here and   [warpzone](https://qiita.com/warpzone) on Qiita posted the first Python scripts I saw to take advantage of it. bbostock's also featured MQTT publishing for integration with Home Assistant.

For reasons that I still can't figure out, neither script worked for me on a Pi 4 or Pi Zero W. The firmware on my Meters was updated from 2.4 to 2.5 as I was starting to work with them. That apparently caused the device model names (WOSensorTH) to not be visible when doing a BLE scan, although the MACs still were. It initially appeared that the firmware upgrade may have been the cause for my Meters failing to work with the scripts.

When OpenWonderLabs [posted](https://github.com/OpenWonderLabs/python-host/blob/master/switchbot_meter_py3.py) an new script that worked with my Meters, I used that a starting point to create my own, resulting in sbm2mqtty. I tested that with my original Pi Zero W set up as well as a Pi 3B+ with fresh Raspbian Buster Lite. bbostock's and warpzone's scripts run successfully on the 3B+, as well.

So, my best guess is that the problem was something with the environments on the Pi4 and Pi Zero W caused by OpenWonderLabs somewhat complicated dependency installation recommendations for python-host. 

### Installation

sbm2mqtt needs the BluePy and Paho MQTT libraries. Run the following commands on a fresh installation of Raspbian Buster Lite:

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python3-pip libglib2.0-dev
$ sudo pip3 install bluepy
$ sudo pip3 install paho-mqtt
```

Create a directory called `switchbot` containing the files:

`sbm2mqtt.py` 

`sbm2mqtt_config.py`







