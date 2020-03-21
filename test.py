from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit, send
import os
from game import Game

from collections import deque

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {}  # dict to track active rooms
EMPTY_ROOMS = deque()
PLAYERS = []


@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    if len(EMPTY_ROOMS):
        room_id = EMPTY_ROOMS.popleft()
        gm = ROOMS.get(room_id)
        gm.add_player(request.sid)
    else:
        gm = Game(
            team_size=data['size'],
            player=request.sid
        )
        room_id = gm.game_id
        EMPTY_ROOMS.append(room_id)
        ROOMS[room_id] = gm
    join_room(room_id)
    print 'The game has created. Waiting opponents.'
    while not gm.is_full():
        pass
    emit('join_room', {'room': room_id}, room=room_id)

@socketio.on('game_move')
def battle(data):
    """Make battle"""
    room = data['room']
    choice = data['symbol']
    gm = ROOMS.get(room)
    player = request.sid
    gm.set_choice(player, choice)
    print gm.playerChoices
    print 'ROOMS', ROOMS
    print 'EMPTY_ROOMS', EMPTY_ROOMS
    while not gm.is_choices():
        pass
    results = gm.get_result()
    emit('game_res', results, room=player)


if __name__ == '__main__':
    socketio.run(app, debug=os.getenv('DEBUG'))