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

class ErukarServer(WebSocketServerProtocol):
    PollTime = 0.25

    def __init__(self):
        self.shard = Shard()
        self.shard.activate()
        self.shard.subscribe('Evan')

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        asyncio.ensure_future(self.poll_responses_for('Evan'))

    async def poll_responses_for(self, uid):
        while True:
            messages = await self.shard.get_outbound_messages()
            self.sendMessage(messages, False)
            await asyncio.sleep(ErukarServer.PollTime)

    async def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            self.shard.consume_command(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ErukarServer

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
