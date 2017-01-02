from erukar import *
import readline, os, sys, threading
import numpy as np

sys.path.append(os.getcwd() + '/hubs')

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
        if msgs: 
            print('\n'.join(msgs))

        self.timer.cancel()
        self.start()

mtracker = MessageTracker(w.interface, alias)
mtracker.start()

while True:
    print('-' * 64)
    line = input('> ')
    res = w.interface.execute(alias, line)
