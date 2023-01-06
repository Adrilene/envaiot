# EnvAIoT - Environment for modelling and simulating Adaptive IoT Systems

This repository contains the EnvAIoT tool's code. This tool assists IoT system designers, engineers, architects, and developers in the design phase of development by focusing on the system's self-adaptation feature and allows them to model and test the effectiveness of their adaption techniques. This paper will describe the architecture as well as how to utilise the tool locally.

## Architecture
Each folder in this repository corresponds to a different component of EnvAIoT. They are as follows:
1. **Configurator**, who is in charge of verifying the model and configuring the other components.
2. **Simulator**, which is in charge of simulating the operation of the IoT system.
3. **Observer** and **Effector** collaborate to accomplish the adaptation. The former monitors and analyses the system, whilst the latter plans and executes the adaptation.

Each component is implemented as an API, thus, the user interact with system performing requests. All of them were implemented using Flask, a Python framework for web services. 

### Configurator
This component is divided into two layers: *Controller* and *Validator*. The former contains the endpoints, while the latter is utilised to validate the modelling. 
There are three endpoints:
+ */configure_all*, receives the modelling of the entire IoT system. 
+ */configure_simulator*, receives the modelling of the resources and communication parts.
+ */configure_adapter*, receives the modelling of the communication, scenarios and strategies. 

The validation procedure begins when a request is received. The names of the devices (which must be in Pascal case), the presence of all keys, and the accuracy of the references in the "senders" key are all checked for the simulator modelling. It examines the modelling of both normal and adaptation scenarios, the presence of the keys, and the accuracy of the names of the adaptation scenarios (pascal case).
When the validation is finished and it is all correct, Configurator sends a request to each component to configure them. 
### Simulator
Besides the endpoint to configure (used by the Configurator), Simulator also provides the following:
+ */devices_list*, it returns the list of all devices instatiated 
+ */\<device\>/status, it has two ways of using it. First, it is possible to know a device's status (specified in \<device\>), using a GET method. Second, it is possible to change a device status (specified in \<device\>), using a POST method.
+ */\<device\>/send_message*, it receives a message for a device (specified in \<device\>) to send it. Optionally, the user can add the receiver of the message.




docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
