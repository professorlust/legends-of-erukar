class Connection:
    def __init__(self, addr, emit):
        self.playernode = None
        self.addr = addr
        self.sid = None
        self.http_port = None
        self.emit = emit

    def add_playernode(self, pn):
        self.playernode = pn
        self.uid = pn.uid

    def is_origin(self, request):
        if hasattr(request, 'sid'):
            return request.sid == self.sid
        return request.environ['REMOTE_PORT'] == self.http_port

    def is_finalized(self):
        return self.sid is not None and self.http_port is not None

    def tell(self, msg_type, msg):
        if self.sid is not None:
            self.emit(msg_type, msg, room=self.sid)
        else: print('ERROR! no sid found')

    def uid(self):
        return '' if not self.playernode else self.playernode.uid
