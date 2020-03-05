#!/usr/bin/env python3
# 
# sbm2mqtt.py
# ronschaefer https://github.com/ronschaeffer
#
# Based in part on https://github.com/OpenWonderLabs/python-host,
#   https://github.com/bbostock/Switchbot_Py_Meter & https://qiita.com/warpzone/items/11ec9bef21f5b965bce3.
# Portions copyright 2017-present WonderLabs, Inc. <support@wondertechlabs.com>
#
from bluepy.btle import Scanner, DefaultDelegate
import binascii
import datetime
import paho.mqtt.client as mqtt

# Import configuration variables from sbm2mqtt_config.py file - Must be in the same folder as this script
from sbm2mqtt_config import mqtt_host, mqtt_port, mqtt_timeout, mqtt_client, mqtt_user, mqtt_pass, mqtt_topic

# SwitchBot UUID - See https://github.com/OpenWonderLabs/python-host/wiki/Meter-BLE-open-API
service_uuid = 'cba20d00-224d-11e6-9fb8-0002a5d5c51b'

class DevScanner(DefaultDelegate):
    def __init__( self ):
        DefaultDelegate.__init__(self)

    # Scan for a build list of SwitchBots with attributes
    def scan_loop(self):
        dev_list =[]
        scanner = Scanner().withDelegate(DevScanner())
        devices = scanner.scan(10.0)

        for dev in devices:
            mac = 0
            for (adtype, desc, value) in dev.getScanData():
                if desc == '16b Service Data':
                    model = binascii.a2b_hex(value[4:6])
                    mode  = binascii.a2b_hex(value[6:8])
                    if len(value) == 16:
                        tempFra = int(value[11:12].encode('utf-8'), 16) / 10.0
                        tempInt = int(value[12:14].encode('utf-8'), 16)
                        if tempInt < 128:
                            tempInt *= -1
                            tempFra *= -1
                        else:
                            tempInt -= 128
                        tempc = tempInt + tempFra
                        humidity = int(value[14:16].encode('utf-8'), 16) % 128
                        battery = int(value[8:10].encode('utf-8'), 16)
                    else:
                        tempc = 0
                        humidity = 0
                        battery = 0
                elif desc == 'Complete 128b Services' and value == service_uuid :
                    mac = dev.addr

            if mac != 0 :
                dev_list.append([mac, model.decode('utf-8'), mode, tempc, humidity, battery])
    
        # Print Switchbot Meter state and publish MQTT
        for (mac, dev_type, mode, tempc, humidity, battery) in dev_list:
            if dev_type == 'T':
                now = datetime.datetime.now()
                print("\nMAC: "+mac)
                print("  Temp: "+str(tempc)+"\xb0C")
                print("  Humidity: "+str(humidity)+"%")
                print("  Battery: "+str(battery)+"%")

                # MQTT publish as JSON
                time_now = now.strftime("%Y-%m-%d %H:%M:%S")
                msg_data = '{"time":\"' + time_now + '\","temperature":' + str(tempc) + ',"humidity":' + str(humidity) + ',"battery":' + str(battery) +'}'
                print("\n  Publishing MQTT payload to "+mqtt_topic+mac+" ...\n\n    "+msg_data)
                mqttc = mqtt.Client(mqtt_client)
                mqttc.username_pw_set(mqtt_user, mqtt_pass)
                mqttc.connect(mqtt_host, mqtt_port)
                mqttc.publish(mqtt_topic+mac, msg_data, 1) 

def main():
    
    print ("\nScanning for SwitchBot Meters...")
    scan = DevScanner()
    dev_list = scan.scan_loop()

    print ("\nFinished.\n")

if __name__ == "__main__":
    main()