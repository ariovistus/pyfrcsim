import socketserver
import socket
import threading
from typing import (
    Callable
)
from google.protobuf.message import (
    Message
)
from gazebo.msgs import (
    Packet
)

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self):
        self.socket = None
        self.server = None

    def connect(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.create_connection((host, port))
        self._make_streams()

    def connect_and_wait(self, host: str, port: int):
        self.host = host
        self.port = port
        while True:
            try:
                self.socket = socket.create_connection((host, port))
                break
            except socket.timeout as ex:
                logger.warning("Cannot connect, retrying in five seconds.", exc_info=1)
        self._make_streams()

    def _make_streams(self):
        self.rfile = self.socket.makefile('r')
        self.wfile = self.socket.makefile('w')

    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        if self.server is not None:
            self.server.shutdown()
            self.server = None

    def serve(self, callback: Callable[[Connection], None]):
        class Handler(socketserver.StreamRequestHandler):
            def __init__(hself):
                hself.callback = callback

            def handle(self):
                conn = Connection()
                conn.rfile = hself.rfile
                conn.wfile = hself.wfile
                hself.callback(conn)

        def _serve():
            self.server = socketserver.TCPServer(("", 0), Handler) 
            self.server.serve_forever()
        thread = threading.Thread(target=_serve)
        thread.start()
        
    def raw_read(self):
        # todo: determine api
        return None

    def read(self) -> Packet:
        # todo: determine api
        return None
        
    def write(self, message: Message):
        # todo: pull in protobuf
        pass

    def write_packet(self, message: Message):
        # todo: figure out where packet.proto is
        pass
