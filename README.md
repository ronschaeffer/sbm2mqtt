# sbm2mqtt

Grab SwitchBot Meter data from Bluetooth Low Energy advertisements and publish them to an MQTT topic for use with Home Assistant, etc.

19 MAR 21: Added Docker option. Will update the README shortly

![Doorbell & notifications](image.png?raw=true)

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

OpenWonderLabs published the open API for SwitchBot Meters in late 2019. [bbostock](https://github.com/bbostock) here and   [warpzone](https://qiita.com/warpzone) on Qiita posted the first Python scripts I saw to taking advantage of it. bbostock's script also featured MQTT publishing for integration with Home Assistant.

For reasons that I still can't figure out, neither script worked for me on a Pi 4 or Pi Zero W. The firmware on my Meters was updated from 2.4 to 2.5 as I was starting to work with them. That caused the device model names (WOSensorTH) to not be visible when doing a BLE scan, although the MACs still were. It initially appeared that the firmware upgrade may have been the cause for my Meters failing to work with the scripts.

When OpenWonderLabs [posted](https://github.com/OpenWonderLabs/python-host/blob/master/switchbot_meter_py3.py) a new script that worked with my Meters, I used it as a starting point to create my own, resulting in sbm2mqtty. I tested that with my original Pi Zero W set up as well as on a Pi 3B+ with fresh Raspbian Buster Lite. bbostock's and warpzone's scripts run successfully on the 3B+, as well.

So, my best guess is that the original failure with bbostock's and warpzone's scripts was something to due with the environments on the Pi4 and Pi Zero W caused by OpenWonderLabs' somewhat complicated dependency installation recommendations for python-host.

I suggest that you don't first follow OpenWonderLabs' dependency installation recommendations for python-host. They are not necessary for sbm2mqtt and may have been the cause of my earlier failures.

### Operation

sbm2mqtt works like this:

- Scan for Bluetooth Low Energy devices, looking for SwitchBot Meters.
- For each SwitchBot Meter, grab the MAC address, temperature, humidity and battery level from the BLE advertisement.
- Publish the temperature, humidity and battery level for each SwitchBot Meter separately to an MQTT topic that includes the MAC address.
- Print the values to the terminal (if not running in the background) and save them to a log.
- If you also configure Home Assistant with MQTT sensors for the sbm2mqtt MQTT topics, HA updates the states of those sensors with every new MQTT message.

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

```
sbm2mqtt.py
sbm2mqtt_config.py
```

You don't need to edit `sbm2mqtt.py`. Edit `sbm2mqtt_config.py` with your settings for:

```python
# MQTT Settings
mqtt_host = 'xxx.xxx.xxx.xxx'
mqtt_port = xxxx
mqtt_timeout = 30
mqtt_client = 'sbm2mqtt'
mqtt_user = 'xxxxxx'
mqtt_pass = 'xxxxxx'
mqtt_topic = 'switchbot_meter'
```

Execute sbm2mqtt in the terminal, and note the MAC addresses of any SwitchBot meters it finds.

If you want to integrate with Home Assistant, add three ```sensor:``` entries to ```configuration.yaml``` for each Meter, as follows:

```yaml
sensor:
- platform: mqtt
  name: 'name_of_this_meter_temperature'
  state_topic: 'switchbot_meter/xx:xx:xx:xx:xx:xx' # MAC address of this meter
  value_template: '{{ value_json.temperature }}'
  unit_of_measurement: '°C' # Change to '°F' as appropriate
- platform: mqtt
  name: 'name_of_this_meter_humidity'
  state_topic: 'switchbot_meter/xx:xx:xx:xx:xx:xx' # MAC address of this meter
  value_template: '{{ value_json.humidity }}'
  unit_of_measurement: '%'
  icon: mdi:water-percent
- platform: mqtt
  name: 'name_of_this_meter_battery'
  state_topic: 'switchbot_meter/xx:xx:xx:xx:xx:xx' # MAC address of this meter
  value_template: '{{ value_json.battery }}'
  unit_of_measurement: '%'
  icon: mdi:battery
```

If you have a split configuration, paste in the contents of the ```sensors.yaml``` file to your sensor configuration file and edit appropriately.

### Use

To execute sbm2mqtt in the `switchbot` directory:

```bash
$ sudo python3 sbm2mqtt.py
```

To run sbm2mqtt in the background automatically every five minutes and also log what it's doing (Thanks, bbostock.):

```bash
$ sudo nano /etc/crontab
```

 and add:

```
*/5 *   * * *   pi      sudo python3 /home/pi/switchbot/sbm2mqtt.py >> /home/pi/switchbot/sbm2mqtt.log 2>&1
```

If you have a different user name or used a different directory structure, edit accordingly.

Your output should look something like this:
```
Scanning for SwitchBot Meters...

f5:49:7c:bb:xx:46 @ 2020-03-30 14:26:02
  Temp: 21.0° C
  Humidity: 29%
  Battery: 100%

  Publishing MQTT payload to switchbot_meter/f5:49:7c:bb:xx:46 ...

    {"time":"2020-03-30 14:26:02","temperature":21.0,"humidity":29,"battery":100,"temperature_scale":"C"}

c9:c7:8d:fb:xx:65 @ 2020-03-30 14:26:05
  Temp: 69.8° F
  Humidity: 30%
  Battery: 100%

  Publishing MQTT payload to switchbot_meter/c9:c7:8d:fb:xx:65 ...

    {"time":"2020-03-30 14:26:05","temperature":69.8,"humidity":30,"battery":100,"temperature_scale":"F"}

Finished.
```

That's it. You should be good to go.
