# Tkinter Interface
from Tkinter import *
    
class TextEditor(Text):

    def __init__(self, master):

        self.master = master
        self.root   = master.root

        # Create y-axis scrollbar

        self.y_scroll = master.y_scroll

        # Create textbox

        Text.__init__(self, self.root, padx=5, pady=5,
                            bg="black", fg="white",
                            insertbackground="White",
                            font = "Font",
                            yscrollcommand=self.y_scroll.set,
                            width=100, height=20, bd=0,
                            undo=True, autoseparators=True,
                            maxundo=50 )
        
        self.grid(row=0, column=0, sticky="nsew")
        self.y_scroll.config(command=self.yview)
        self.focus_set()
