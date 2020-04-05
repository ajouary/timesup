from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')

game={'List_of_world':['ritao','anna'],'Room':'team14'}

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    gm = game['List_of_world']
    room = game['Room']
    print(data)
    ROOMS[room] = gm
    join_room(room)

    emit('join_room', {'room': room})

@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    # username = data['username']
    room = data['room']
    if room in ROOMS:
        # add player and rebroadcast game object
        # rooms[room].add_player(username)
        join_room(room)
        send(ROOMS[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

@socketio.on('flip_card')
def on_flip_card(data):
    """flip card and rebroadcast game object"""
    room = data['room']
    card = data['card']
    ROOMS[room].flip_card(card)
    send(ROOMS[room].to_json(), room=room)

if __name__ == "__main__":        # on running python app.py
    #app.run(debug=True)            # run the flask app
    socketio.run(app, debug=True)