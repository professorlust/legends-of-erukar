from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import asyncio, websockets, json, os, sys, datetime

class ErukarServerFactory(WebSocketServerFactory):
    PollTime = 0.5

    async def activate_shard(self, shard):
        print('shard activated')
        self.shard = shard
        self.shard.activate()
        self.clients = {} # eid: client
        asyncio.ensure_future(self.poll_responses())

    async def register(self, client, eid):
        print('Registered eid {}'.format(eid))
        if eid not in self.clients.values():
            self.shard.subscribe(eid)
        self.clients[client] = eid

    async def request_authentication(self, client):
        client.sendMessage(json.dumps({'type': 'authRequest'}).encode('utf8'), False)

    async def confirm_authentication(self, client, payload):
        print('Confirmation received')
        client.sendMessage(json.dumps({'type': 'authConfirmation','authToken': 'asdfasdf'}).encode('utf8'), False)
        await self.register(client, payload['eid'])

    def unregister(self, client):
        print('Unregistered {}'.format(self.clients[client]))
        #self.shard.unsubscribe(self.clients[client])
        #self.clients.pop(client)

    async def poll_responses(self):
        while True:
            for client in self.clients:
                await self.send_update(client)
            await asyncio.sleep(ErukarServerFactory.PollTime)

    async def send_update(self, client):
        eid = self.clients[client]
        async for message in self.shard.get_outbound_messages(eid):
            client.sendMessage(message)


class ErukarServerProtocol(WebSocketServerProtocol):
    async def onConnect(self, request):
        print('Connection establishing at {}'.format(request.peer))

    async def onOpen(self):
        print('Connection established -- requesting authentication')
        await self.factory.request_authentication(self)

    async def onMessage(self, payload, isBinary):
        message = json.loads(payload.decode('utf8')) 
        if 'type' not in message: return

        if message['type'] == 'authenticationConfirmation':
            await self.factory.confirm_authentication(self, message)
        else:
            self.factory.shard.consume_command(message['payload'])

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.unregister(self)

