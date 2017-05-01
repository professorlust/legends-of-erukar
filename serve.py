from erukar import *
import erukar
import asyncio, websockets, json
import datetime

def create_random_character():
    p = Player()
    s = Sword()
    p.inventory.append(s)
    erukar.game.modifiers.Steel().apply_to(s)
    erukar.game.modifiers.Bane().apply_to(s)

    h = Hauberk()
    p.inventory.append(h)
    erukar.game.modifiers.Salericite().apply_to(h)
    return p

def process_state(p, d):
    inv_cmd = Inventory()
    inv_cmd.world = d
    inv_cmd.player_info = p
    inv_res = inv_cmd.execute().result_for(p.uuid)[0]

    stat_cmd = Stats()
    stat_cmd.world = d
    stat_cmd.player_info = p
    stat_res = stat_cmd.execute().result_for(p.uuid)

    return {
        'inventory': inv_res['inventory'],
        'equipment': inv_res['equipment'],
        'vitals': stat_res[0]
    }

async def do_run(websocket, path):
    p = create_random_character()
    d = Dungeon()
    while True:
        data = process_state(p, d)
        await websocket.send(json.dumps(data))
        await asyncio.sleep(5)

start_server = websockets.serve(do_run, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

