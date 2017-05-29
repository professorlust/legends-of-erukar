from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from erukar import *
import logging
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

class ErukarServerFactory(WebSocketServerFactory):
    PollTime = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shard = Shard()
        self.shard.activate()
        self.clients = {} # eid: client
        asyncio.ensure_future(self.poll_responses())

    async def register(self, client, eid):
        print('Registered eid {}'.format(eid))
        self.shard.subscribe(eid)
        self.clients[client] = eid

    async def request_authentication(self, client):
        client.sendMessage(json.dumps({'type': 'authenticationRequest'}).encode('utf8'), False)

    async def confirm_authentication(self, client, payload):
        print('Confirmation received')
        await self.register(client, payload['eid'])

    def unregister(self, client):
        print('Unregistered {}'.format(self.clients[client]))
        #self.shard.unsubscribe(self.clients[client])
        self.clients.pop(client)

    async def poll_responses(self):
        while True:
            for client in self.clients:
                await self.send_update(client)
            await asyncio.sleep(ErukarServerFactory.PollTime)

    async def send_update(self, client):
        eid = self.clients[client]
        payload = await self.shard.get_outbound_messages(eid)
        client.sendMessage(payload)

class ErukarServerProtocol(WebSocketServerProtocol):
    async def onConnect(self, request):
        print('Connection establishing at {}'.format(request.peer))

    async def onOpen(self):
        print('Connection established -- requesting authentication')
        await self.factory.request_authentication(self)

    async def onMessage(self, payload, isBinary):
        message = json.loads(payload.decode('utf8')) 
        if 'type' not in message: return

        if message['type'] == 'interaction':
            self.factory.shard.consume_command(message['payload'])
        if message['type'] == 'authenticationConfirmation':
            await self.factory.confirm_authentication(self, message)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.unregister(self)

if __name__ == '__main__':
    import asyncio

    factory = ErukarServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ErukarServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
