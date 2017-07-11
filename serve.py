from erukar.server.Shard import Shard
import asyncio, websockets, json, os, sys, datetime
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from concurrent.futures import ProcessPoolExecutor

ServerLogger = logging.getLogger('server')
ServerLogger.setLevel(logging.INFO)
fh = logging.FileHandler('server.log')
ServerLogger.addHandler(fh)

from flask import Flask
from flask import request, jsonify, abort
from socketio import Middleware
from flask_socketio import SocketIO, emit, send
from erukar import PlayerNode, Player, Lifeform
import erukar


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
    if con is None: abort(401)
    if con.playernode.status != PlayerNode.CreatingCharacter: abort(403)

    data = request.get_json(force=True)
    if 'step' not in data: abort(400)
    
    if data['step'] == 'bio':
        print(data)
        return "success"
    return jsonify(message="Validation Errors occurred.")

@app.route('/api/templates')
def get_templates():
    def format_template(template):
        return {
            'name': template.name,
            'description': template.description,
            'stats': template.stats,
            'inventory': [x.alias() for x in template.inventory]
        }

    templates = [format_template(t) for t in shard.templates]
    return jsonify(templates)

@app.route('/api/regions')
def get_regions():
    def format(info):
        region = info.instance.dungeon
        return {
            'name': region.name,
            'sovereignty': region.sovereignty,
            'region': region.region, # yo dawg
            'description': region.description,
            'profile': 'Woodlands Dungeon',
        }

    regions = [format(t) for t in shard.starting_region_options]
    return jsonify(regions)


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
    player_schema = erukar.data.models.Player.get(shard.session, uid)
    if player_schema is None:
        return 'Could not find specified UID'

    con.playernode = player_schema.create_new_object()
    return [Shard.format_character_for_list(x) for x in player_schema.characters]

@socketio.on('register')
def ws_register(raw_creds):
    ServerLogger.info('registering {}'.format(raw_creds))
    credentials = json.loads(raw_creds)
    if 'uid' not in credentials: return "Malformed request received"

    con = shard.update_connection(request)
    if erukar.data.models.Player.get(shard.session, credentials['uid']):
        return 'UID {} already exists'.format(credentials['uid'])

    con.playernode = PlayerNode(credentials['uid'],None)
    con.playernode.name = 'Evan'
    player_schema = erukar.data.models.Player.add(shard.session, con.playernode)
    return [Shard.format_character_for_list(x) for x in player_schema.characters]

@socketio.on('launch')
def on_launch(*_):
    con = shard.get_client(request)
    if con is None or not hasattr(con, 'character') or con.character is None:
        if con is not None: print(con.character)
        return
    shard.start_playing(con.playernode, con.character)
    con.tell('launch success' ,'')

@socketio.on('request state')
def on_request_state():
    con = shard.get_client(request)
    if con.playernode is not None and con.playernode.status == PlayerNode.Playing:
        con.tell('update state', shard.get_state_for(con.uid()))
    else: con.tell('specific message', 'Not playing')

@socketio.on('select character')
def ws_select_character(raw_data):
    data = json.loads(raw_data)
    if 'id' not in data: return "Character does not exist"
    cid = data['id']

    con = shard.get_client(request)
    if con is None: return "Connection is invalid"
    
    character = erukar.data.models.Character.select(shard.session, cid, con.uid())

    if character is not None:
        con.character = character.create_new_object()
        return 'Successfully selected {}'.format(con.character.name)
    return 'No character was found!'

@socketio.on('add new character')
def on_add_character(*_):
    con = shard.update_connection(request)
    if con.playernode is not None:
        con.playernode.status = PlayerNode.CreatingCharacter
        return 'success'
    return 'Cannot add character -- Not logged in'

@socketio.on('finalize new character')
def on_finish_character_creation(raw_data):
    data = json.loads(raw_data)
    ServerLogger.info(type(data))
    if 'stats' not in data or 'bio' not in data:
        return 'invalid payload'

    con = shard.get_client(request)
    if con is None: return 'Client is not logged in'

    built = Lifeform.build_from_payloads(data['stats'], data['bio'])
    player_schema = erukar.data.models.Player.get(shard.session, con.playernode.uid)
    schema = erukar.data.models.Character.create_from_object(shard.session, built, player_schema)
    schema.add_or_update(shard.session)

@socketio.on('send command')
def on_command_receipt(cmd):
    ServerLogger.info(cmd)
    shard.consume_command(request, cmd)


if __name__ == "__main__":
    print('shard activating')

    socketio.run(app, host="0.0.0.0")
    for con in shard.clients:
        con.tell('end', {})

