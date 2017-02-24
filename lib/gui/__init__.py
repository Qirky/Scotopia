
#stdlib
import sys

# Tkinter Interface
from Tkinter import *
import ttk
import tkFont
import tkFileDialog
import tkMessageBox

# Scotopia GUI Modules
from TextEditor import TextEditor
from MenuBar import MenuBar
from CameraView import CameraCanvas

class App:

    def __init__(self, server_instance):

        # We are running a server instance

        self.server = server_instance

        self.__peers = 0

        # Set up master widget  

        self.root = Tk()
        self.root.title("Scotopia")
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.kill )

        # Set monospace font depending on O/S

        if sys.platform.startswith('win'):
            fonttype = "Consolas" # windows

        elif sys.platform.startswith('darwin'):
            fonttype = "Monaco" # mac

        else: fonttype = "Courier New" # linux or other
        
        self.font = tkFont.Font(font=(fonttype, 16), name="Font")

        # Set up text box
        self.y_scroll = Scrollbar(self.root)
        self.y_scroll.grid(row=0, column=1, sticky='nsew')
        self.text = TextEditor(self)

        # Add menubar
        
        self.menu = MenuBar(self)

        # Add canvas

        self.canvas = CameraCanvas(self)

        # main program loop func

        self.mainloop = self.root.mainloop

    # Webcam functionality

    def setup(self, camera_instance):
        self.server.set_camera( camera_instance )
        self.add_image("local", camera_instance)
        self.root.title("Scotopia @ {}:{}".format(*self.server.get_address()))
        self.server.start()

    def nextPeerID(self):
        self.__peers += 1
        return self.__peers

    def add_peer(self, ip_addr):
        """ Connects to another Scotopia instance and adds to address book """
        new_peer = self.server.new_peer(ip_addr)

        if new_peer != None:

            self.add_image("peer" + str(self.nextPeerID()), new_peer)

    def add_image(self, name, camera_instance):
        lbl = Label(self.canvas, bg="white", bd=5)
        self.canvas.images[name] = (camera_instance, lbl)
        lbl.pack()

    def kill(self):

        for camera, label in self.canvas.images.values():

            camera.close()

        self.server.close()

        self.root.destroy()
        

if __name__ == "__main__":

    App.mainloop()
