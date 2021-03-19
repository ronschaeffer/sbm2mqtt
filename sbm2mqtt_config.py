#!/usr/bin/env python3

# Use environement variables or replace with your own values
# Environment variables override contents of this file
# Place in same folder as sbm2mqtt.py

import os

# MQTT settings
mqtt_host = os.environ.get("MQTT_HOST", "127.0.0.1")
mqtt_port = int(os.environ.get("MQTT_PORT", "1883"))
mqtt_timeout = int(os.environ.get("MQTT_TIMEOUT", "30"))
mqtt_client = os.environ.get("MQTT_CLIENT", "sbm2mqtt")
mqtt_user = os.environ.get("MQTT_USER", "xxxxxx")
mqtt_pass = os.environ.get("MQTT_PASS", "xxxxxx")
mqtt_topic = os.environ.get("MQTT_TOPIC", "switchbot_meter")
