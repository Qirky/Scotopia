# Tkinter Interface
from Tkinter import *
    
class TextEditor(Text):

    def __init__(self, master, **kwargs):

        self.master = master
        self.root   = master.root

        # Create y-axis scrollbar

        self.y_scroll = master.y_scroll

        # Create textbox

        Text.__init__(self, self.root,
                      bg="black", fg="white",
                      insertbackground="White",
                      width=kwargs.get("width", 100),
                      height=kwargs.get("height", 10),
                      bd=kwargs.get("bd", 0),
                      padx=5, pady=5,
                      font = "Font",
                      yscrollcommand=self.y_scroll.set,
                      undo=True, autoseparators=True, maxundo=50 )
        
        self.grid(row=0, column=0, sticky="nsew")
        self.y_scroll.config(command=self.yview)
        self.focus_set()
