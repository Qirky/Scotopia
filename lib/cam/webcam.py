import socket
import cPickle as pickle
import numpy
import cv2
from PIL import Image, ImageTk
from threading import Thread
from time import sleep


class VideoStream(object):
    blank = numpy.zeros([200,200,3], dtype='uint8')
    def __init__(self):
        self._frame = self.blank
        self._w = 200
        self._h = 200
        self.islooking = False
        self.address = ('localhost', 59123)
    def update_address(self, **kwargs):
        self.address = (kwargs.get("host", self.address[0]),
                        kwargs.get("port", self.address[1]))
    def read(self):
        return self._frame
    def width(self):
        return self._w
    def height(self):
        return self._h
    def get_last_frame(self):
        return self._frame
    def show(self, frame="frame"):
        """ Shows the current frame in a cv2 window """
        cv2.imshow(frame, self._frame)
    def close(self):
        cv2.destroyAllWindows()

class Camera(VideoStream):

    def __init__(self):

        # Inheritance
        VideoStream.__init__(self)

        # Get webcam & width + height
        self.src = cv2.VideoCapture(0)
        self._w = int(self.src.get(3))
        self._h = int(self.src.get(4))

        # Test if webcam is present
        ret, _ = self.src.read()

        if not ret:

            raise Exception("No web cam detected")

        # Keep track of what camera "this" camera/client is looking at
        self.view = None

        # Setup threading
        self.running = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):

        while self.running:

            # Capture frame-by-frame
            ret, f = self.src.read()

            # Flip frame in the x-axis

            f = cv2.flip(f, 1)

            # Convert to RGB for Tkinter

            self._frame = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)                

            # 30fps

            sleep(0.03)

    def close(self):
        self.running = False
        self.src.release()
        VideoStream.close(self)

class PeerCam(VideoStream):
    """ Class representing the webcam client on a remote machine """
    def __init__(self, ip, server=None):
        # Inheritance
        VideoStream.__init__(self)
        
        # Setup networking
        self.ip_addr = ip
        self.address = (self.ip_addr, 59123)
        self.socket = socket.socket()

        # Keep info on the local server to send to the peer
        self.local_server = server

        # create  connection
        self.connect()

        # Setup threading
        self.running = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def connect(self):

        # Connect to the remote

        self.socket.connect(self.address)

        # Recv remote address book 
        data = self.socket.recv(2048)

        for ip_addr in data.split():

            if ip_addr not in self.local_server.get_address_book() and ip_addr != self.ip_addr:

                self.local_server.add_new_peer(ip_addr)

        # Push local address book
        self.socket.send(self.local_server.address_book_as_string())

        return
    
    def run(self):

        while self.running:

            # 1. Single integer 1 or 0 if this peer is viewing the local client

            data = self.socket.recv(1)

            # If we receive no data, assume the client is lost

            if len(data):

                self.islooking = bool(int(data))

            else:

                # Remove client from app then exit

                self.local_server.app.remove_peer_by_ip(self.ip_addr)

                return

            # 2. Read the numpy array of the image

            data = self.socket.makefile()

            try:

                self._frame = pickle.load(data)
                
            except:

                self._frame = self.blank    
                
            self._w = int(self._frame.shape[1])
            self._h = int(self._frame.shape[0])

            data.close()

            sleep(0.03)

    def close(self):
        self.running = False
        self.socket.close()
        VideoStream.close(self)

if __name__ == "__main__":

    cam = Camera()

    while True:

        cam.read()
        cam.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.close()
