from erukar.server.Shard import Shard
import asyncio, websockets, json, os, sys, datetime
import logging
from concurrent.futures import ProcessPoolExecutor

from flask import Flask
from flask import request, jsonify, abort
from socketio import Middleware
from flask_socketio import SocketIO, emit, send
from erukar import PlayerNode, Player, Lifeform

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
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

blacklist = []

shard = Shard(emit)
shard.activate()


@app.route('/api/ping')
def do_ping():
    return jsonify({
        'name': shard.properties.Name,
        'url': shard.properties.Url,
        'players': shard.active_players(),
        'maxPlayers': shard.properties.MaxPlayers,
        'description': shard.properties.Description,
        'permadeath': shard.properties.PermaDeath,
        'password': False
    })

@app.route('/validate', methods=['POST'])
def validation():
    con = shard.get_client(request)
    if con is None:
        abort(401)
    if con.playernode.status != PlayerNode.CreatingCharacter:
        abort(403)

    data = request.get_json(force=True)
    if 'step' not in data:
        abort(400)
    
    if data['step'] == 'bio':
        print(data)
        return "success"
    return jsonify(message="Validation Errors occurred.")

@app.route('/character/templates')
def get_templates():
    def format_template(template):
        return {
            'name': template.name,
            'description': template.description,
            'stats': template.stats,
            'inventory': [x.describe() for x in template.inventory]
        }

    templates = [format_template(t) for t in shard.templates]
    return jsonify(templates)


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

@app.route('/character/startcreation', methods=['POST'])
def on_add_character():
    con = shard.update_connection(request)
    if con.playernode is not None:
        con.playernode.status = PlayerNode.CreatingCharacter
        return 'success'
    abort(400)

@app.route('/character/endcreation', methods=['POST'])
def on_finish_character_creation():
    data = request.get_json(force=True)
    if 'stats' not in data or 'bio' not in data:
        abort(400)

    con = shard.get_client(request)
    if con is None: abort(401)

    res = Lifeform.build_from_payloads(data['stats'], data['bio'])
    shard.data.add_character(con.playernode.uid, res)
    _, raw_chars = shard.login(con.playernode.uid)

    characters = [Shard.format_character_for_list(x) for x in raw_chars]
    return jsonify(message="Successfully created character", characters=characters)


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

@socketio.on('login')
def ws_login(raw_creds):
    credentials = json.loads(raw_creds)
    if 'uid' not in credentials:
        return 'Malformed request received'
    uid = credentials['uid']

    con = shard.update_connection(request)
    playernode, raw_chars = shard.login(uid)
    if playernode is None:
        return 'Could not find specified UID'

    con.playernode = playernode
    return [Shard.format_character_for_list(x) for x in raw_chars]

@socketio.on('register')
def ws_register(raw_creds):
    credentials = json.loads(raw_creds)
    if 'uid' not in credentials: return "Malformed request received"

    con = shard.update_connection(request)
    if shard.data.player_exists(credentials['uid']):
        return 'UID {} already exists'.format(credentials['uid'])

    con.playernode = PlayerNode(credentials['uid'],None)
    shard.data.add_player(con.playernode)
    _, raw_chars = shard.login(credentials['uid'])
    return [Shard.format_character_for_list(x) for x in raw_chars]

@socketio.on('launch')
def on_launch(*_):
    print('launch received')
    con = shard.get_client(request)
    if con is None or not hasattr(con, 'character') or con.character is None:
        print(con)
        if con is not None: print(con.character)
        return
    shard.start_playing(con.playernode, con.character)
    con.tell('launch success' ,'')

@socketio.on('request state')
def on_request_state():
    print('requesting state')
    con = shard.get_client(request)
    if con.playernode is not None and con.playernode.status == PlayerNode.Playing:
        con.tell('update state', shard.get_state_for(con.uid()))
    else: con.tell('specific message', 'Not playing')

@socketio.on('send command')
def on_command_receipt(cmd):
    shard.consume_command(request, cmd)


if __name__ == "__main__":
    print('shard activating')

    socketio.run(app, host="0.0.0.0")
    for con in shard.clients:
        con.tell('end', {})

