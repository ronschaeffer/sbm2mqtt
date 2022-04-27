# sbm2mqtt

Grab SwitchBot Meter data from Bluetooth Low Energy advertisements and publish them to an MQTT topic for use with Home Assistant, etc. sbm2mqtt supports any number of meters.

![Switchbot & Home Assistant card](image.png?raw=true)

- Based in part on [OpenWonderLabs/python-host](https://github.com/OpenWonderLabs/python-host), [Switchbot_Py_Meter](https://github.com/bbostock/Switchbot_Py_Meter) and [switchbot-meter.py](https://qiita.com/warpzone/items/11ec9bef21f5b965bce3).
- Intended for use with [Home Assistant](https://github.com/home-assistant/home-assistant.io) but applicable to any system which can use MQTT.
- Applies to SwitchBot Meter devices with the BLE UUID [cba20d00-224d-11e6-9fb8-0002a5d5c51b](https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API). I don't know if all SwitchBot Meter hardware and firmware versions share the same UUID.

Tested with:

- Pi Zero W, Pi 3B+ and Pi 4B running Raspbian Buster and Python 3.7.3
- SwitchBot Meters with firmware 2.5 & 2.6
- Local MQTT broker
- Home Assistant versions 0.106 to 2021.3 (optional) 

Some users have reported success with Ubuntu systems. If you use sbm2mqtt on a system other than a Pi running Raspbian/Raspberry Pi OS, please raise an issue with details or edit this README file and create a pull request. 

### Operation

sbm2mqtt works like this:

- Scan for SwitchBot Meter BLE advertisements.
- For each SwitchBot Meter, grab the MAC address, temperature, humidity and battery level from the advertisement.
- Publish the temperature, humidity and battery level for each SwitchBot Meter separately to an MQTT topic that includes the MAC address.
- Print the values to the terminal (if not running in the background) and save them to a log.
- If you also configure Home Assistant with MQTT sensors for the sbm2mqtt MQTT topics, HA updates the states of those sensors with every new MQTT message.

### Installation

First, download and unzip or clone all files in the repository. You can install and run sbm2mqtt as a Docker container or directly on a Raspberry Pi.

#### Docker

Build the Docker image:

```
docker build . -t sbm2mqtt
```

To spin up the Docker container, either use the following command replacing the environmental variable defaults with your own:

```
docker run --rm --net=host --privileged -it -e MQTT_HOST=127.0.0.1 -e MQTT_PORT=1883 -e MQTT_USER=xxxxxx -e MQTT_PASS=xxxxxx REPORTING_INTERVAL=300 sbm2mqtt
```

Or, edit the `sbm2mqtt_config.py` file with your own information and just use:

```
docker run --rm --net=host --privileged -it sbm2mqtt
```

Available environmental variables

| Variable             | Default         | Description                                        |
| -------------------- | --------------- | -------------------------------------------------- |
| `MQTT_HOST`          | 127.0.0.1       | IP address of the MQTT broker                      |
| `MQTT_PORT`          | 1883            | Port of the MQTT broker                            |
| `MQTT_CLIENT`        | sbm2mqtt        | Name of the MQTT client                            |
| `MQTT_USER`          | xxxxxx          | MQTT user name                                     |
| `MQTT_PASS`          | xxxxxx          | MQTT password                                      |
| `MQTT_TOPIC`         | switchbot_meter | MQTT topic to monitor in Home Assistant, etc.      |
| `REPORTING_INTERVAL` | 300             | Time in seconds between each execution of sbm2mqtt |

#### Raspberry Pi OS

sbm2mqtt needs the BluePy and Paho MQTT libraries. Run the following commands on a fresh installation of Raspbian Buster:

```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install python3-pip libglib2.0-dev
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

To execute sbm2mqtt in the `switchbot` directory:

```bash
$ sudo python3 sbm2mqtt.py
```

To run sbm2mqtt in the background automatically every five minutes and also log what it's doing:

```bash
$ sudo nano /etc/crontab
```

 and add:

```
*/5 *   * * *   pi      sudo python3 /home/pi/switchbot/sbm2mqtt.py >> /home/pi/switchbot/sbm2mqtt.log 2>&1
```

If you have a different user name or used a different directory structure, edit accordingly.

### Output

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

### Integration with Home Assistant

Execute sbm2mqtt and note the MAC addresses of any SwitchBot meters it finds.

Add three ```sensor:``` entries to ```configuration.yaml``` for each Meter, as follows:

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
