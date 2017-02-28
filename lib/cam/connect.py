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
            at that client. """

        # self.server = ThreadedServer
        # self.request = socket
        # self.client_address = (address, port)

        # 1. On initial connection, return the address book of peers of *this* peer

        self.request.sendall(" ".join(self.server.address_book))

        # 2. Get the address book of the requesting peer

        data = self.request.recv(2048)

        for ip_addr in data.split():

            if ip_addr not in self.server.address_book:

                self.server.add_new_peer(ip_addr)

        # 3. Continually send webcam data to the requesting client

        while self.server.running and self.server.connected_to(self.client_address):

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

                break

        return

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 59123

        self.__server = ThreadedServer((self.host, self.port), RequestHandler)
        self.server_thread = Thread(target=self.__server.serve_forever)
        self.server_thread.daemon = True

        self.__server.address_book = {}
        self.__server.add_new_peer = self.add_new_peer
        self.__server.remove_peer  = self.remove_peer
        self.__server.connected_to = self.connected_to

        self.app = None

    def set_camera(self, camera_instance):
        """ Gives the serve a reference to the webcam viewer object and updates
            the 'localhost' entry in its address book dictionary. """
        camera_instance.update_address(host=self.__server.server_address[0])
        self.__server.address_book[camera_instance.address[0]] = self.__server.camera = camera_instance

    def connected_to(self, address):
        """ Takes an address tuple and returns True if the address is in the address book """
        return address[0] in self.__server.address_book

    def add_new_peer(self, ip_addr):
        """ Adds a new peer to the server address book if that address
            does not already exist """
        if ip_addr not in self.__server.address_book:
            try:
                # Create new peer instance
                peer = PeerCam(ip_addr, server=self)
            except socket.error:
                print("Could not connect to {}: the target host did not respond".format(ip_addr))
                peer = None
            # Add the peer to the gui
            if peer is not None:
                self.__server.address_book[ip_addr] = peer
                self.app.add_peer(peer)
            return peer
        else:
            return None

    def remove_peer(self, ip_addr):
        if ip_addr in self.__server.address_book:
            self.__server.address_book[ip_addr].close()
            del self.__server.address_book[ip_addr]

    def get_address_book(self):
        return self.__server.address_book

    def address_book_as_string(self):
        return " ".join(self.__server.address_book)

    def get_address(self):
        return self.__server.server_address

    def start(self):
        self.__server.running = True
        self.server_thread.start()

    def close(self):
        self.__server.running = False
        self.__server.shutdown()
        self.__server.server_close()
