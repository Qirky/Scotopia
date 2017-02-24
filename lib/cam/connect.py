import cPickle as pickle
import SocketServer
import socket
from threading import Thread
from webcam import PeerCam

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class RequestHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        """ Is called when another client requests the current image
            and a boolean of whether this local machine is "looking"
            at that client.
            TODO
            sends a 1 or 0 followed by a serial of the webcam image """

        # self.server = ThreadedServer
        # self.request = socket
        # self.client_address = (address, port)

        while self.server.running:

            try:

                # Send a 1 or 0 if the requesting client is being "viewed"
                
                self.request.send(str(int(self.server.camera.view == self.client_address[0])))

                # Send the image

                data = self.server.camera.get_last_frame()

                if data is not None:

                    f = self.request.makefile()

                    pickle.dump(data, f, protocol=-1)

                    f.close()

            except socket.error:

                return

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 59123

        self.__server = ThreadedServer((self.host, self.port), RequestHandler)
        self.server_thread = Thread(target=self.__server.serve_forever)
        self.server_thread.daemon = True

    def set_camera(self, camera_instance):
        self.__server.camera = camera_instance

    def new_peer(self, ip_addr):
        try:
            peer = PeerCam(ip_addr)
        except socket.gaierror:
            print("Could not connect to {}: the target host did not respond".format(ip_addr))
            peer = None
        return peer

    def get_address(self):
        return self.__server.server_address

    def start(self):
        self.__server.running = True
        self.server_thread.start()

    def close(self):
        self.__server.running = False
        self.__server.shutdown()
        self.__server.server_close()
