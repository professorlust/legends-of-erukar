from erukar import *
import readline, os, sys, threading
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

w = Shard()
w.activate()

alias = 'Evan'
w.subscribe(alias)

class MessageTracker:
    def __init__(self, interface, alias):
        self.timer = None
        self.interface = interface
        self.alias = alias

    def start(self):
        self.timer = threading.Timer(0.1, self.check_for_messages)
        self.timer.start()

    def check_for_messages(self):
        msgs = self.interface.get_messages_for(self.alias)
        if self.timer:
            self.timer.cancel()
        self.start()

mtracker = MessageTracker(w.interface, alias)
mtracker.check_for_messages()

while True:
    line = input('')
    print('-' * 64)
    res = w.interface.receive(alias, line)
