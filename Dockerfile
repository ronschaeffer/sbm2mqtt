# docker build . -t sbm2mqtt
# docker run --rm --net=host --privileged -it sbm2mqtt
FROM python:3.7
RUN apt-get update && apt-get install -y bluez bluetooth
RUN pip install bluepy paho-mqtt
ENTRYPOINT sh docker_entrypoint.sh
COPY . .
