from Tkinter import Menu

class MenuBar(Menu):

    def __init__(self, master):

        self.app    = master
        self.root   = master.root

        Menu.__init__(self, self.root)

        self.config(font="Font")

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="New Document",  command=lambda: None,     accelerator="Ctrl+N")
        filemenu.add_command(label="Open",          command=lambda: None,     accelerator="Ctrl+O")
        filemenu.add_command(label="Save",          command=lambda: None,     accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...",    command=lambda: None )
        self.add_cascade(label="File", menu=filemenu)

        connectmenu = Menu(self, tearoff=0)
        connectmenu.add_command(label="Connect to Peer", command=self.add_peer)
        self.add_cascade(label="Connect", menu=connectmenu)

        master.root.config(menu=self)

    def add_peer(self):
        """ Opens a dialog window to enter an IP address """

        text = TextEntry(self, title="Scotopia")

        ip_addr = text.result

        if ip_addr:

            peer = self.app.server.add_new_peer(ip_addr)

        return

class PeerMenu(Menu):
    """ Drop down menu that appears when clicking on a peer """
    def __init__(self, master):
        self.app = master.app
        Menu.__init__(self, master.root, tearoff=0)
        self.add_command(label="Next", command=lambda: None)
        self.add_command(label="Back", command=lambda: None)
        self.add_separator()
        self.add_command(label="Remove", command=self.remove_clicked_peer)

    def remove_clicked_peer(self):
        peer = self.app.last_clicked_peer
        if peer != "local":
            self.app.canvas.images[peer].camera.close()
            self.app.canvas.images[peer].destroy()
            self.app.server.remove_peer(self.app.canvas.images[peer].camera.address[0])
            del self.app.canvas.images[peer]
        return
        

    

from Tkinter import Button, Label, Entry
import tkSimpleDialog

class TextEntry(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Enter IP Address: ").grid(row=0)

        self.text = Entry(master)
        self.text.grid(row=0, column=1)

        return self.text

    def apply(self):
        self.result = self.text.get()
