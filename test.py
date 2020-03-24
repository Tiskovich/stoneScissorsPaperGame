import os
import time
from collections import deque

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit

from game import Game, choices

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

ROOMS = {}
EMPTY_ROOMS = deque()
PLAYERS = []


@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    player = request.sid
    if len(EMPTY_ROOMS):
        room_id = EMPTY_ROOMS.popleft()
        gm = ROOMS.get(room_id)
        gm.add_player(request.sid)
    else:
        gm = Game(
            team_size=data['size'],
            player=player
        )
        room_id = gm.game_id
        EMPTY_ROOMS.append(room_id)
        ROOMS[room_id] = gm
    join_room(room_id)
    print 'The game has created. Waiting opponents.'
    while not gm.is_full():
        time.sleep(1)
    emit('join_room', {'room': room_id, 'player_id': player}, room=room_id)


@socketio.on('game_move')
def battle(data):
    """Make battle"""
    room = data['room']
    choice = data['symbol']
    gm = ROOMS.get(room)
    player = request.sid
    gm.set_choice(player, choice)
    while not gm.is_choices():
        time.sleep(1)
    results = gm.get_result()
    results['your_results'] = results.get(player)
    results['your_choice'] = gm.playerChoices.get(player)
    opponent_choices = [v for _, v in gm.playerChoices.iteritems() if _ != player]
    results['opponent_choices'] = opponent_choices
    emit('game_res', results, room=player)


@socketio.on('terminate_session')
def terminate_session(data):
    """Terminate session"""
    room = data['room']
    player_id = data['player_id']
    gm = ROOMS.get(room)
    gm.set_choice(player_id, choices.LEAVE_GAME)
    emit('disconnect')
    print 'Client {} leave game'.format(player_id)


if __name__ == '__main__':
    socketio.run(app, debug=os.getenv('DEBUG'))