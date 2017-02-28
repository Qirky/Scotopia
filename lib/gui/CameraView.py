from Tkinter import Canvas, Label
from PIL import Image, ImageTk
from MenuBar import PeerMenu

class basicEvent:
    def __init__(self, h, w):
        self.height = h
        self.width = w

class CameraCanvas(Canvas):
    def __init__(self, master, **kwargs):
        self.app   = master
        self.root  = master.root

        # Set up main canvas

        Canvas.__init__(self, self.root,
                        background="black",
                        **kwargs)

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.old_height = self.height

        self.bind("<Configure>", self.on_resize)
        
        self.grid(row=1, column=0, sticky="nsew" )

        # Set up label info

        self.label_border_size = 5
        self.padding = 10

        self.images = {}

        self.update()

    def on_resize(self, event=None):
        # determine the ratio of old width/height to new width/height

        eventh = event.height if event is not None else self.old_height
        eventw = event.width  if event is not None else self.width

        newheight = min(eventh, self.root.winfo_height() / 3)
        newwidth  = min(eventw, self.app.text.winfo_width())
        
        wscale = float(newwidth)/self.width
        hscale = float(newheight)/self.height

        self.width  = newwidth
        self.height = newheight

        # resize the canvas 
        self.config(width=self.width, height=self.height)

        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

    def get_size(self):
        return self.root.winfo_width(), self.root.winfo_height()

    # Possible to just "update" the image with the data?
    def convert_to_photo_image(self, camera, height=0):
        """ Converts a numpy array to a PhotoImage """

        # Read in the array
        img = Image.fromarray( camera.read() )

        # Get the size
        if height > 0:
            
            size = (int(camera.width() * float(height)/camera.height()), height)

        else:

            size = (camera.width(), camera.height())

        img = img.resize(size)

        # Convert resized image to PhotoImage
        return ImageTk.PhotoImage(image=img)


    def update(self):
        """ Updates the images in the canvas """

        if len(self.images) > 0:

            # Get mouse co-ordinates

            mousex = self.winfo_pointerx()
            mousey = self.winfo_pointery()

            # Get width & height

            w = self.width
            h = self.height - ((self.label_border_size + self.padding) * 2)

            if h <= 0:

                h = self.old_height - ((self.label_border_size + self.padding) * 2)

                self.on_resize()

            offset = w / (len(self.images) + 1)

            # Store the address + port of the peer being "viewed"

            view = None

            # Iterate over the connected webcams
            
            for i, lbl in enumerate(self.images.values()):

                # Get the webcam image but make sure the height is correct

                img = self.convert_to_photo_image(lbl.camera, height=h)
                lbl.image = img

                # Get co-ordinates

                lblx1 = lbl.winfo_rootx()
                lblx2 = lblx1 + img.width()

                lbly1 = lbl.winfo_rooty()
                lbly2 = lbly1 + img.height()

                client_islooking = (lblx1 < mousex < lblx2 and lbly1 < mousey < lbly2)

                # Store the IP address

                if client_islooking:

                    view = lbl.camera.address[0]

                # If the peer and client are looking at each other, show it blue

                if lbl.camera.islooking and client_islooking:

                    lbl.config(image=img, bg="blue")

                # If this peer is "looking" at the client, show it green

                elif lbl.camera.islooking:

                    lbl.config(image=img, bg="green")

                # If mouse is hovering on a label, send info to other client and update colours

                elif client_islooking:

                    lbl.config(image=img, bg="red")

                # Show it white

                else:

                    lbl.config(image=img, bg="white")

                # Make sure it's in the right place

                lbl.place(x=offset + (i * offset), y=self.padding, anchor="n")

            # Update the reference to the address of the camera being viewed

            self.images['local'].camera.view = view      

        self.after(50, self.update)

class ClientLabel(Label):
    """ TKinter Label that holds webcam images """
    def __init__(self, root, *args, **kwargs):
        self.app = root.app
        Label.__init__(self, root, **kwargs)
        self.bind("<Button-1>", self.popup_menu)
        self.menu = PeerMenu(root)
        self.camera = None
        self.name   = None

    def define(self, name, camera_instance):
        """ Setup with name and camera """
        self.name = name
        self.camera = camera_instance
        return self

    def popup_menu(self, event):
        """ Create popup menu and store the name of this peer """
        try:
            self.app.last_clicked_peer = self.name
            self.menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.menu.grab_release()
            

