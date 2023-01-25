python3 ./Configurator/run.py & \
python3 ./Effector/run.py & \
python3 ./Observer/run.py & \
python3 ./Simulator/run.py & \
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
