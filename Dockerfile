FROM python:3.6

# Copy source
COPY . /app
RUN chmod +x /app/run.sh
WORKDIR /app

RUN apt-get update && apt-get install -y libbluetooth-dev python-pip libglib2.0-dev mosquitto-clients redis-server
RUN pip3 install -r requirements.txt

#python -m site --user-site
#sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper

ENTRYPOINT ["./run.sh"]

# docker build -t ter_haar/ble_gateway .
# docker run -it ter_haar/ble_gateway
# docker start -a -i container_id
# docker exec -ti container_id bash -c "exec bash"
