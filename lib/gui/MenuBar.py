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

            self.app.add_peer(ip_addr)

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
