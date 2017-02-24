import socket
import cPickle as pickle
import numpy
import cv2
from PIL import Image, ImageTk
from threading import Thread
from time import sleep

BLANK_IMAGE = numpy.zeros([200,200,3], dtype='uint8')

class VideoStream(object):
    def empty_frame(self):
        """ Returns a numpy array of zeros """
        return BLANK_IMAGE
    def read(self):
        if self._frame is not None:
            return self._frame
        else:
            return self.empty_frame()
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

        # Get webcam & width + height
        self.src = cv2.VideoCapture(0)
        self._w = int(self.src.get(3))
        self._h = int(self.src.get(4))

        self._frame = None

        # Test if webcam is present
        
        ret, _ = self.src.read()

        if not ret:

            raise Exception("No web cam detected")
        
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
    def __init__(self, ip):
        # Setup networking
        self.address = (ip, 59123)
        self.socket = socket.socket()
        self.socket.connect(self.address)

        self._w = None
        self._h = None

        self.running = True
        self.thread = Thread(target=self.run)
        self.thread.start()
    
    def run(self):

        while self.running:

            data = self.socket.makefile()

            try:
                self._frame = pickle.load(data)
            except:
                self._frame = self.empty_frame()
                
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
