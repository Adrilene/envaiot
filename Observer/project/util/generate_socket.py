import socketio

sio = socketio.Client()

@sio.on('all')
def on_message(data):
    print(f'\n{data}\n')


@sio.event
async def connect():
    print("I'm connected!")


@sio.event
def connect_error(err):
    print(err)
    print("\nThe connection failed!\n")
    sio.disconnect()


@sio.event
def disconnect():
    print("I'm disconnected!")
