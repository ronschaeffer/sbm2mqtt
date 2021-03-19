# docker build . -t sbm2mqtt
# docker run --rm --net=host --privileged -it -e MQTT_HOST=192.168.1.10 -e MQTT_USER=bob -e MQTT_PASS=waffles sbm2mqtt
FROM python:3.7
RUN apt-get update && apt-get install -y bluez bluetooth
RUN pip install bluepy paho-mqtt
ENV \
    MQTT_HOST=127.0.0.1 \
    MQTT_PORT=1883 \
    MQTT_USER=xxxxxx \
    MQTT_PASS=xxxxxx \
    MQTT_CLIENT=sbm2mqtt \
    MQTT_TOPIC=switchbot_meter \
    REPORTING_INTERVAL=300
      # in seconds
ENTRYPOINT sh docker_entrypoint.sh
COPY . .
