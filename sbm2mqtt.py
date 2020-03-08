#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# sbm2mqtt.py https://github.com/ronschaeffer/sbm2mqtt
#
# Based in part on:
#   https://github.com/OpenWonderLabs/python-host
#   https://github.com/bbostock/Switchbot_Py_Meter
#   https://qiita.com/warpzone/items/11ec9bef21f5b965bce3

from bluepy.btle import Scanner, DefaultDelegate
import datetime
import binascii
import paho.mqtt.client as mqtt

# Import configuration variables from sbm2mqtt_config.py file
# Must be in the same folder as this script

from sbm2mqtt_config import mqtt_host, mqtt_port, mqtt_timeout, \
    mqtt_client, mqtt_user, mqtt_pass, mqtt_topic

# SwitchBot UUID
# See https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API

service_uuid = 'cba20d00-224d-11e6-9fb8-0002a5d5c51b'


class ScanDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)

  # Scan for BLE device advertisements, filter out ones which are not SwitchBot Meters & convert the service data to binary

    def handleDiscovery(
        self,
        dev,
        isNewDev,
        isNewData,
        ):

        for (adtype, desc, value) in dev.getScanData():

            # Check for devices with Switchnot devices

            if adtype == 7 and value == service_uuid:
                mac = dev.addr
                for (adtype, desc, value) in dev.getScanData():

                    # Check for model "T" (54) in 16b service data

                    if len(value) == 16 and value[4:6] == '54':

                        # Convert service data from hex to binary
                        # See BLE API docs and warpzone link above for value mapping

                        binvalue = binascii.unhexlify(value)

            # Get temperature and related characteristics

                        # Absolute value of temp

                        temperature = (binvalue[6] & 0b01111111) \
                            + (binvalue[5] & 0b00001111) / 10

                        # Is temp negative?

                        if not binvalue[6] & 0b10000000:
                            temperature = -temperature

                        # C or F?

                        if not binvalue[7] & 0b10000000:
                            temp_scale = 'C'
                        else:
                            temp_scale = 'F'

                            # Convert to F

                            temperature = round(temperature * 1.8 + 32,
                                    1)

            # Get other info

                        humidity = binvalue[7] & 0b01111111
                        battery = binvalue[4] & 0b01111111

            # Get current time

                        time = \
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'
                                )

            # Print info to terminal

                        print '\n' + mac + ' @ ' + str(time)
                        print '  Temp: ' + str(temperature) + '\xb0' \
                            + temp_scale
                        print '  Humidity: ' + str(humidity) + '%'
                        print '  Battery: ' + str(battery) + '%'

            # MQTT publish as JSON

                        msg_data = '{"time":"' + time \
                            + '","temperature":' + str(temperature) \
                            + ',"humidity":' + str(humidity) \
                            + ',"battery":' + str(battery) \
                            + ',"temperature scale":"' + temp_scale \
                            + '"}'
                        print '\n  Publishing MQTT payload to ' \
                            + mqtt_topic + mac + ''' ...

    ''' \
                            + msg_data
                        mqttc = mqtt.Client(mqtt_client)
                        mqttc.username_pw_set(mqtt_user, mqtt_pass)
                        mqttc.connect(mqtt_host, mqtt_port)
                        mqttc.publish(mqtt_topic + mac, msg_data, 1)


def main():

    print '\nScanning for SwitchBot Meters...'
    scan = scanner = Scanner().withDelegate(ScanDelegate())
    scanner.scan(10.0)

    print '''
Finished.
'''


if __name__ == '__main__':
    main()