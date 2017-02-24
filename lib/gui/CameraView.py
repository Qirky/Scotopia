from Tkinter import Canvas, Label
from PIL import Image, ImageTk

class CameraCanvas(Canvas):
    def __init__(self, master):
        self.app   = master
        self.root  = master.root

        Canvas.__init__(self, self.root,
                        background="black")
        
        self.grid(row=1, column=0, sticky="nsew" )

        self.images = {}

        self.update()

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

            w, h = self.get_size()

            h /= 4

            offset = w / (len(self.images) + 1)

            # Iterate over the connected webcams
            
            for i, value in enumerate(self.images.values()):

                camera, lbl = value

                # Get the webcam image but make sure the height is correct

                img = self.convert_to_photo_image(camera, height=h)
                lbl.image = img

                # Get co-ordinates

                lblx1 = lbl.winfo_rootx()
                lblx2 = lblx1 + img.width()

                lbly1 = lbl.winfo_rooty()
                lbly2 = lbly1 + img.height()

                # If mouse is hovering on a label, send info to other client and update colours

                if lblx1 < mousex < lblx2 and lbly1 < mousey < lbly2:

                    lbl.config(image=img, bg="red")

                else:

                    lbl.config(image=img, bg="white")

                lbl.place(x=offset + (i * offset), y=10, anchor="n")

        self.after(50, self.update)