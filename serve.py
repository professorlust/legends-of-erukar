from erukar.system import Shard, PlayerNode, Player, Lifeform
import asyncio, websockets, json, os, sys, datetime
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from concurrent.futures import ProcessPoolExecutor

from flask import Flask
from flask import request, jsonify, abort
from socketio import Middleware
from flask_socketio import SocketIO, emit, send
import erukar

logger = logging.getLogger('debug')

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
    })

@app.route('/api/details')
def get_details():
    active_players = [{
        'name': c.playernode.name,
        'character': getattr(c.playernode.character, 'name', ''),
        'level': getattr(c.playernode.character, 'level', '')
    } for c in shard.clients if c.playernode]
    return jsonify({
        'name': shard.properties.Name,
        'url': shard.properties.Url,
        'players': active_players,
        'maxPlayers': shard.properties.MaxPlayers,
        'adminDetails': shard.properties.AdminDetails,
        'motd': shard.properties.Description,
        'permadeath': 'Enabled' if shard.properties.PermaDeath else 'Disabled',
        'version': shard.ErukarVersion,
    })

@app.route('/validate', methods=['POST'])
def validation():
    return jsonify('ok')
#   con = shard.get_client(request)
#   if con is None: abort(401)
#   if con.playernode.status != PlayerNode.CreatingCharacter: abort(403)

#   data = request.get_json(force=True)
#   if 'step' not in data: abort(400)
#   
#   if data['step'] == 'bio':
#       print(data)
#       return "success"
#   return jsonify(message="Validation Errors occurred.")

@app.route('/api/templates')
def get_templates():
    def format_template(template):
        return {
            'name': template.name,
            'description': template.description,
            'stats': template.stats,
            'inventory': [format_item_for_template(x, template) for x in template.inventory],
            'skills': [format_skill_for_template(x, template) for x in template.skills]
        }

    templates = [format_template(t) for t in shard.templates]
    return jsonify(templates)

def format_item_for_template(item, template):
    formatted = {
        'name': item.alias(),
        'type': item.__module__
    }
    if item.material: 
        formatted['material'] = item.material.__module__
    equipment_slot = next((slot for slot in template.equipment_types if item == getattr(template, slot, None)), None)
    if equipment_slot:
        formatted['slot'] = equipment_slot
    return formatted

def format_skill_for_template(skill, template):
    return {
        'name': skill.Name,
        'type': skill.__module__,
        'level': skill.level,
        'description': skill.current_level_description()
    }


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
    player_schema = erukar.data.model.Player.get(shard.session, uid)
    if player_schema is None:
        return 'Could not find specified UID'

    con.playernode = player_schema.create_new_object()
    return [Shard.format_character_for_list(x) for x in player_schema.characters]

@socketio.on('register')
def ws_register(raw_creds):
    credentials = json.loads(raw_creds)
    if 'uid' not in credentials: return "Malformed request received"

    con = shard.update_connection(request)
    if erukar.data.model.Player.get(shard.session, credentials['uid']):
        return 'UID {} already exists'.format(credentials['uid'])

    con.playernode = PlayerNode(credentials['uid'],None)
    con.playernode.name = credentials['uid']
    player_schema = erukar.data.model.Player.add(shard.session, con.playernode)
    return [Shard.format_character_for_list(x) for x in player_schema.characters]

@socketio.on('launch')
def on_launch(*_):
    con = shard.get_client(request)
    if con is None or not hasattr(con, 'character') or con.character is None:
        if con is not None: print('Connection has no character')
        return
    con.playernode.update_socket(con)
    shard.start_playing(con.playernode, con.character)
    con.tell('launch success' ,'')

@socketio.on('request state')
def on_request_state():
    con = shard.get_client(request)
    if con.playernode is not None and con.playernode.status == PlayerNode.Playing:
        con.tell('update state', shard.get_state_for(con.playernode))
    else: con.tell('specific message', 'Not playing')

@socketio.on('select character')
def ws_select_character(raw_data):
    data = json.loads(raw_data)
    if 'id' not in data: return "Character does not exist"
    cid = data['id']

    con = shard.get_client(request)
    if con is None: return "Connection is invalid"
    
    character = erukar.data.model.Character.select(shard.session, cid, con.uid())

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
    if 'stats' not in data or 'bio' not in data:
        return 'invalid payload'

    con = shard.get_client(request)
    if con is None: return 'Client is not logged in'

    built = Lifeform.build_from_payloads(data['stats'], data['bio'])
    player_schema = erukar.data.model.Player.get(shard.session, con.playernode.uid)
    schema = erukar.data.model.Character.create_from_object(shard.session, built, player_schema)
    if 'template' in data:
        schema.apply_template(data['template'])
    schema.add_or_update(shard.session)

    character = erukar.data.model.Character.select(shard.session, schema.id, con.playernode.uid)
    if character is not None:
        con.character = character.create_new_object()
        return 'Successfully selected {}'.format(con.character.name)
    return 'No character was found!'

@socketio.on('send command')
def on_command_receipt(cmd, *_):
    shard.consume_command(request, cmd)
