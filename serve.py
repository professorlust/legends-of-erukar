from erukar import *
import erukar
import asyncio, websockets, json, os, sys, datetime
import numpy as np

config_directories = [
    'world/sovereignties',
    'world/regions',
    'world/hubs',
    'scripts',
    'server'
]

for cd in config_directories:
    sys.path.append(os.getcwd() + '/config/' + cd)

class WebsocketServer:
    def __init__(self):
        self.shard = Shard()
        self.shard.activate()
        self.shard.subscribe('Evan')

    async def handle_outbound(self, ws):
        '''Handles all outbound messages'''
        message = await self.shard.get_outbound_messages()
        await ws.send(message)

    async def handle_inbound(self, ws):
        message = await ws.recv()
        await self.shard.consume_message(message)

    async def handler(self, ws, path):
        inbound = asyncio.ensure_future(self.handle_inbound(ws))
        outbound = asyncio.ensure_future(self.handle_outbound(ws))
        done, pending = await asyncio.wait(
            [inbound, outbound],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()   

    def start(self):
        start_server = websockets.serve(self.handler, '127.0.0.1', 5678)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

ws = WebsocketServer()
ws.start()

#def process_state(p, d):
#    inv_cmd = Inventory()
#    inv_cmd.world = d
#    inv_cmd.player_info = p
#    inv_res = inv_cmd.execute().result_for(p.uuid)[0]
#
#    stat_cmd = Stats()
#    stat_cmd.world = d
#    stat_cmd.player_info = p
#    stat_res = stat_cmd.execute().result_for(p.uuid)
#
#    return {
#        'inventory': inv_res['inventory'],
#        'equipment': inv_res['equipment'],
#        'vitals': stat_res[0]
#    }
#
#async def do_run(websocket, path):
#    p = create_random_character()
#    d = Dungeon()
#    while True:
#        data = process_state(p, d)
#        await websocket.send(json.dumps(data))
#        await asyncio.sleep(5)
#
#start_server = websockets.serve(do_run, '127.0.0.1', 5678)
#
#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()
#
