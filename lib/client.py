from gui import App
from cam import Camera, Server

# Create application with a ref to a server
client = App(Server())

# Set up local camera
client.setup(Camera())

# Run application
client.mainloop()
