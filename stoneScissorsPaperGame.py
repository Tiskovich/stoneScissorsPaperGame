import os
import time
from collections import deque

from flask import request
from flask_socketio import SocketIO, join_room, emit

from app import flask_app
from app.game import GameRoom, choices

socketio = SocketIO(flask_app)

ROOMS = {}
EMPTY_ROOMS = deque()
PLAYERS = []


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    results = {}
    player_sid = request.sid
    player_name = data.get('player_name')
    print data
    print 'CREATE GAME', player_name
    if len(EMPTY_ROOMS):
        room_id = EMPTY_ROOMS.popleft()
        gm = ROOMS.get(room_id)
    else:
        gm = GameRoom(
            team_size=data['size'],
            player=player_sid,
            # player_name=player_name,
        )
        room_id = gm.game_id
        EMPTY_ROOMS.append(room_id)
        ROOMS[room_id] = gm
    print 'The room with id {} has been created'.format(room_id)
    print ROOMS
    gm.add_player(player_name, request.sid)
    join_room(room_id)
    print 'The game has created. Waiting opponents.'
    while not gm.is_full_game():
        time.sleep(1)
    results['stats'] = gm.get_player_stats(player_name)
    emit('join_room', {'room': room_id, 'player_sid': player_sid, 'results': results}, room=room_id)


@socketio.on('game_move')
def battle(data):
    """Make battle"""
    results = {}
    room_id = int(data['room'])
    player_name = data.get('player_name', 'Unknown')
    choice = data['symbol']
    player_sid = request.sid
    gm = ROOMS.get(room_id)
    gm.set_choice(player_name, choice)
    while not gm.is_all_choices():
        time.sleep(1)
    while not gm.is_calculated:
        time.sleep(1)
        gm.calc_results()
        gm.is_calculated = True
    results['your_results'] = gm.get_player_result(player_name)
    results['your_choice'] = choice
    results['opponent_choices'] = gm.get_opponents_choices()
    results['stats'] = gm.get_player_stats(player_name)
    print results
    emit('game_res', results, room=player_sid)


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
    socketio.run(flask_app, debug=os.getenv('DEBUG'))