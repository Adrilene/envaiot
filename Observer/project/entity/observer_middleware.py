import json
import threading
import socketio
import requests
import asyncio
from project.util.data import add_new
from .observer import Observer
import socketio


class ObserverMiddleware(threading.Thread, Observer):
    def __init__(self, config):
        threading.Thread.__init__(self)
        Observer.__init__(self, config)
        self.sio = socketio.Client()
        self.sio.on('all', self.handler)
        self.config = config["connection_config"]
        self.topic = self.config["topic"]
        self.token = self.get_socket_token()
        self.call_one = True

    def run(self):
        asyncio.run(
            self.sio.connect(f'{self.config["host"]}:{self.config["port"]}/?token={self.token}',
                        transports=["websocket"],
                        namespaces=['/all'],
                        socketio_path='socket.io')
        )

    def handler(self, data): 
        current_scenario = data[self.topic]
        print(f"Current Scenario: {current_scenario} - {self.scenario_running}")
        print(f"Exceptional Scenario: {self.exceptional_scenario}")
        is_essential_scenarios = False

        is_essential_scenarios = self.is_essential_scenarios(current_scenario)
        if is_essential_scenarios:
            self.essential_scenarios = add_new(
                self.essential_scenarios, current_scenario
            )

        except_scen = self.check_essential_exceptional()
        print(f"essential Scenario: {list(self.essential_scenarios)} \n\n")
        if except_scen and self.call_one:
            print("==== Cenário excepcional ====")
            requests.get(
                url=f"http://localhost:4002/adapt?scenario={self.scenario_running}"
            )
            self.call_one = False

        if self.check_normal_scenario(current_scenario) and except_scen:
            print("==== Cenário NORMAL ====")
            requests.get(
                url=f"http://localhost:4002/behave_normal?scenario={self.scenario_running}"
            )
            self.essential_scenarios = []
            self.call_one = True
            self.scenario_running = ""
            except_scen = False

    def stop(self):
        raise SystemExit()

    def get_token_dojot(self):
        url = f'{self.config["host"]}:{self.config["port"]}/auth'
        payload = {"username": self.config["user"], "passwd": self.config["password"]}
        headers = {"Content-Type": "application/json"}
        return requests.post(url, headers=headers, json=payload).json()["jwt"]

    def get_socket_token(self):
        url = f'{self.config["host"]}:{self.config["port"]}/stream/socketio'
        token = self.get_token_dojot()
        headers = {"Authorization": f"Bearer {token}"}
        return requests.request("GET", url, headers=headers).json()["token"]



# @sio.event
# def on_connect(self):
#     print("I'm connected!")

# @sio.event
# def on_disconnect(self):
#     print("I'm disconnected!")


def on_message(data):
    global self
    print(dir(data))
    print(data)
    print(self)

    current_scenario = data[self.topic]
    print(f"Current Scenario: {current_scenario} - {self.scenario_running}")
    print(f"Exceptional Scenario: {self.exceptional_scenario}")
    is_essential_scenarios = False

    is_essential_scenarios = self.is_essential_scenarios(current_scenario)
    if is_essential_scenarios:
        self.essential_scenarios = add_new(
            self.essential_scenarios, current_scenario
        )

    except_scen = self.check_essential_exceptional()
    print(f"essential Scenario: {list(self.essential_scenarios)} \n\n")
    if except_scen and self.call_one:
        print("==== Cenário excepcional ====")
        requests.get(
            url=f"http://localhost:5002/adapt?scenario={self.scenario_running}"
        )
        self.call_one = False

    if self.check_normal_scenario(current_scenario) and except_scen:
        print("==== Cenário NORMAL ====")
        requests.get(
            url=f"http://localhost:5002/behave_normal?scenario={self.scenario_running}"
        )
        self.essential_scenarios = []
        self.call_one = True
        self.scenario_running = ""
        except_scen = False

    print(f"\n{data}\n")



# @sio.on("all")
# def on_message(data):
#     global self

#     print(self)
#     print(dir(self))
#     print(self.topic)

#     current_scenario = data[self.topic]
#     print(f"Current Scenario: {current_scenario} - {self.scenario_running}")
#     print(f"Exceptional Scenario: {self.exceptional_scenario}")
#     is_essential_scenarios = False

#     is_essential_scenarios = self.is_essential_scenarios(current_scenario)
#     if is_essential_scenarios:
#         self.essential_scenarios = add_new(
#             self.essential_scenarios, current_scenario
#         )

#     except_scen = self.check_essential_exceptional()
#     print(f"essential Scenario: {list(self.essential_scenarios)} \n\n")
#     if except_scen and self.call_one:
#         print("==== Cenário excepcional ====")
#         requests.get(
#             url=f"http://localhost:5002/adapt?scenario={self.scenario_running}"
#         )
#         self.call_one = False

#     if self.check_normal_scenario(current_scenario) and except_scen:
#         print("==== Cenário NORMAL ====")
#         requests.get(
#             url=f"http://localhost:5002/behave_normal?scenario={self.scenario_running}"
#         )
#         self.essential_scenarios = []
#         self.call_one = True
#         self.scenario_running = ""
#         except_scen = False

#     print(f"\n{data}\n")


# @sio.event
# async def connect():
#     print("I'm connected!")


# @sio.event
# def connect_error(err):
#     print(err)
#     print("\nThe connection failed!\n")
#     sio.disconnect()


# @sio.event
# def disconnect():
#     print("I'm disconnected!")
