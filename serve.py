from erukar.server.Server import *
from erukar.server.Shard import Shard
import asyncio, websockets, json, os, sys, datetime
import logging
from concurrent.futures import ProcessPoolExecutor

from flask import Flask
from flask import request, jsonify, abort
from flask_socketio import SocketIO, emit, send
from erukar import PlayerNode

#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

config_directories = [
    'world/sovereignties',
    'world/regions',
    'world/hubs',
    'scripts',
    'server'
]

for cd in config_directories:
    sys.path.append(os.getcwd() + '/config/' + cd)

app = Flask(__name__)
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

blacklist = []

'''Routes'''

@app.route('/')
def hello():
    return 'Hello'

@app.route('/wiki/<string:article>')
def wiki(article):
    return jsonify({ 
        'title': 'Salericite Ore',
        'atAGlance': {
            'title': 'Salericite',
            'sections': [
                {'title':'Arcane Properties', 'values': ['Arcane enhancement']},
                {'title':'Phase', 'values': ['Solid']},
                {'title':'Melting Point', 'values': ['Unknown']},
                {'title':'Boiling Point', 'values': ['Unknown']},
                {'title':'Density', 'values': ['18.3 g / cubic cm']},
                {'title':'Known Alloys', 'values': ['None']},
                {'title':'Known Deposits', 'values': ['~~Oridel~~, ~~Iuria~~', '~~Honeptys Flatlands::honeptys-flatlands~~, ~~Nothren~~']},
                {'title':'Discovered By', 'values': ['Alvedor Zelongo, 13 CA']},
            ],
        },
        'sections': []
    })

@app.route('/login', methods=['POST'])
#@cross_origin()
def login():
    # Get the data from the post
    data = request.get_json(force=True)
    if 'uid' not in data:
        abort(400)
    uid = data['uid']

    con = shard.update_connection(request)
    playernode, raw_chars = shard.login(uid)
    if playernode is None:
        abort(401)

    con.playernode = playernode
    characters = [Shard.format_character_for_list(x) for x in raw_chars]
    return jsonify(message="Successfully registered as {}".format(uid), characters=characters)

@app.route('/character/select', methods=['POST'])
def select_character():
    data = request.get_json(force=True)
    if 'id' not in data:
        abort(400)
    cid = data['id']

    con = shard.get_client(request)
    if con is None: 
        abort(401)
    
    _, characters = shard.login(con.uid())
    con.character = next((x for x in characters if x.id == cid), None)

    if con.character is not None:
        print('{} has selected {}!'.format(con.uid(), con.character.name))
        return 'Successfully selected a character'

    return 'No character was found!'


'''Websocket Endpoints'''

@socketio.on('connect')
def on_connect():
    addr = request.environ['REMOTE_ADDR']
    if addr in blacklist:
        print('{} was found in the blacklist and was rejected'.format(addr))
    shard.update_connection(request)

@socketio.on('disconnect')
def on_disconnect():
    shard.disconnect(request)

@socketio.on('launch')
def on_launch(*_):
    con = shard.get_client(request)
    if con is None or not hasattr(con, 'character') or con.character is None:
        return
    shard.start_playing(con.playernode, con.character)
    con.tell('launch success' ,'')

@socketio.on('request state')
def on_request_state():
    con = shard.get_client(request)
    if con.playernode is not None and con.playernode.status == PlayerNode.Playing:
        con.tell('update state', shard.get_state_for(con.uid()))

@socketio.on('send command')
def on_command_receipt(cmd):
    shard.consume_command(request, cmd)

'''Helpers'''

if __name__ == '__main__':
    shard = Shard(emit)
    shard.activate()

    socketio.run(app, host="0.0.0.0")
    for con in shard.clients:
        con.tell('end', {})
